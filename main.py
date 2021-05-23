import json
import datetime
import requests
import consts
import time
from datetime import datetime
from twilio.rest import Client

headers = {
    "USER_AGENT" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
}


####### FUNCTION TO TAKE INPUT
def take_input():
    inputs = dict()
    ids = dict()


    ####### GET LIST OF STATES & ASK USER TO SELECT THEIR CHOICE
    response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/states", headers = headers).json()
    
    state_list = [(state["state_id"], state["state_name"]) for state in response["states"]]
    for state in state_list:
        print(f'{state[0]}. {state[1]}')
    ids["state"] = int(input("\nEnter State index from the list: "))
    inputs["state"] = [state[1] for state in state_list if state[0]==ids["state"]][0]

    ####### GET LIST OF DISTRICTS & ASK USER TO SELECT THEIR CHOICE
    response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/"+str(ids["state"]), headers=headers).json()
    
    district_list = [(district["district_id"], district["district_name"]) for district in response["districts"]]
    print("\n")
    for district in district_list:
        print(f'{district[0]}. {district[1]}')    
    ids["district"] = int(input("\nEnter District index from the list: "))
    inputs["district"] = [district[1] for district in district_list if district[0]==ids["district"]][0]

    ####### GET LIST OF PREFERRED CENTRES
    print("\n")
    inputs["centres"] = input("Enter preferred centres (Format: Kallara, Kaipuzha):").split(', ')
    
    ####### GET PHONE NUMBER TO BE NOTIFIED    
    print("\n")
    inputs["phone"] = "+91"+input("Enter the number to which alert to be sent (10 digits): ")
    if len(inputs["phone"]) != 13:
        print("Invalid number. Exiting...")
        exit()

    ####### GET AGE LIMIT    
    print("\n")
    age_choice = input("Enter the age limit:\n1. 18-44\n2. 45+\nChoice (1 or 2): ")
    if age_choice == "1":
        inputs["age_limit"] = "18"
    elif age_choice == "2":
        inputs["age_limit"] = "45"
    else:
        print("Invalid Choice. Exiting...")
        exit()

    ####### GET DOSE CHOICE
    print("\n")
    inputs["dose_choice"] = input("Enter Dose number (1 or 2): ")
    if inputs["dose_choice"] not in ["1","2"]:
        print("Invalid Choice. Exiting...")
        exit()
    
    return inputs, ids

def find_apps(ids, inputs, flag):
    today = datetime.now().strftime("%d-%m-%Y")
    params = {
        'district_id' : ids['district'],
        'date' : today
    }

    ####### CALL API AND RETRIEVE 7 DAY DATA FOR THE DISTRICT    
    response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict", params=params, headers=headers).json()
    
    if response["centers"]: 
        ####### IF ANY CENTRE AVAILABLE:
        centres_avail = [centre["name"] for centre in response["centers"]]

        centres_need = []
        for centre_n in inputs["centres"]:
            for centre_a in centres_avail:
                if centre_n.lower() in centre_a.lower():
                    centres_need.append(centre_a)
        ### centres_need contains list of full centre names we need

        centre_details = [centre for centre in response["centers"] if centre["name"] in centres_need]

        ####### app_list CONTAINS PER DAY PER DOSE CAPACITY OF EACH CENTRE REQUIRED
        app_list = {
            '18': {},
            '45': {}
        }

        for centre in centre_details:
            if centre["sessions"]:
                for session in centre["sessions"]:
                    if session["available_capacity_dose"+inputs["dose_choice"]] != 0:
                        app_list[str(session["min_age_limit"])].setdefault(centre["name"],[]).append(
                                {
                                "date" : session["date"],
                                "capacity" : session["available_capacity"],
                                "dose1" : session["available_capacity_dose1"],
                                "dose2" : session["available_capacity_dose2"]
                            }
                        )
        
        ####### IF SLOTS FOUND AND NOTIFICATION NOT YET SENT, SEND NOTIFICATION
        if app_list[inputs["age_limit"]] and flag == 0:
            send_notif(inputs, app_list)
            print(datetime.now().strftime("%d %b, %H:%M") + " Slots available! Notification sent")
            flag = 1
        ####### IF SLOTS FOUND AND NOTIFICATION ALREADY SENT, DO NOT SEND NOTIFICATION
        elif app_list[inputs["age_limit"]] and flag == 1:
            print(datetime.now().strftime("%d %b, %H:%M") + " Notification already sent")
        ####### IF NO SLOTS FOUND, PRINT MESSAGE
        elif not app_list[inputs["age_limit"]]:
            print(datetime.now().strftime("%d %b, %H:%M") + " Sorry! All slots booked at required centres") 
            flag = 0
        
        return flag

    else:
        ####### IF NO CENTRES AVAILABLE, PRINT MESSAGE
        print(datetime.now().strftime("%d %b, %H:%M") + " Sorry! No centres available.")
        flag = 0
        return flag

def send_notif(inputs, app_list):
    msg="Hi! "

    for centre in app_list[inputs["age_limit"]].keys():
        msg += ", ".join([ str(sess["dose"+inputs["dose_choice"][-1:]]) for sess in app_list[inputs["age_limit"]][centre] ])
        msg += " slots available on "
        msg += ", ".join([ sess["date"].split("-")[0] for sess in app_list[inputs["age_limit"]][centre] ])
        msg += (" dates respectively at " + centre + ". ")

    client = Client(consts.ACCOUNT_SID, consts.AUTH_TOKEN)
    message = client.messages.create(
                                body=msg,
                                from_ = consts.FROM,
                                to = inputs["phone"]
                            )

    # call = client.calls.create(
    #                         url='https://api.twilio.com/cowbell.mp3',
    #                         from_ = consts.FROM,
    #                         to = inputs["phone"]
    #                     )

def mainfunc():
    print("~~~~~~~~ Welcome to Covid Vaccine Notifier ~~~~~~~~\n")
    inputs, ids = take_input()

    print("\nLoading", end='')
    for i in range(5):
        print(".", end='')
        time.sleep(1)
    print("\n")
    flag = 0

    while True:
        flag = find_apps(ids, inputs, flag)
        if flag == 0:
           time.sleep(3*60)
        elif flag == 1:
            time.sleep(5*60)


if __name__ ==  "__main__":
    try:
        mainfunc()
    except KeyboardInterrupt:
        print("\n\nInterrupt Caught. Exiting......")