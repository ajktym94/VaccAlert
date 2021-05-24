# Vacc Alert

A COVID-19 vaccine slot availability notifier.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)

### Introduction
 Vacc Alert is a COVID-19 vaccine slot availability notifier for usage in India built using
 * Python
 * Co-WIN Public APIs (provided by Govt. of India) 
 * Twilio (a cloud communications platform)

 Using this command line tool, people can input their preferences like state, district, preference of centres, age, choice of dose and phone number. The script will then periodically check the availability of slots in the centres of preference and notify the user in the phone number given. The user can then login to the cowin website and book his/her appointment. 

 The script has been designed in such a way that anyone with basic command line proficency can use it easily.

 However, the user has to sign up for a trial account with Twilio and then verify their phone number to recieve messages. Users can also be notified with a missed call if needed.

### Features
* Easy Usage
* No need to waste your time reloading the website.
* Users will be alerted with a simple SMS

### Getting Started

#### Setting Up Twilio
* Sign Up for Twilio [here](https://www.twilio.com/try-twilio).
![Sign Up](https://github.com/ajktym94/VaccAlert/blob/images/img/1_signup.jpg?raw=true)
* Verify your email-id and phone number with Twilio.
* Obtain a trial number by clicking "Get a Trial Number"
![Trial Number](https://github.com/ajktym94/VaccAlert/blob/images/img/2_trial_number.jpg?raw=true)
* In the end, take note of your trial number, Account SID and Auth Token from your dashboard.
![Take note](https://github.com/ajktym94/VaccAlert/blob/images/img/dashboard.jpg?raw=true)

### Installation

1. Clone this repository or download ZIP and extract
2. Open command prompt or terminal and get in to this folder.
```
cd VaccAlert
```
3. Run  ```pip install -r requirements.txt```
4. Edit file named "consts.py" and enter your Twilio Account SID, Auth token and trial number in the following format:
```
ACCOUNT_SID = "<Twilio Account SID>"
AUTH_TOKEN = "<Twilio Auth Token>"
FROM = "<Twilio trial number>"
```
5. If you need to be notified by call, you can uncomment lines 149-153 of the file ```main.py```
5. You are ready to go! 


### Usage

1. Open CMD/Terminal and run ```py main.py```
2. Enter the required details
3. The script will run in the background and you can exit it anytime by pressing ```Ctrl + C```
![Usage](https://github.com/ajktym94/VaccAlert/blob/images/img/usage.jpg?raw=true)
4. Sample SMS below:

![Message](https://github.com/ajktym94/VaccAlert/blob/images/img/msg.jpg?raw=true)