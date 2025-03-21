### Project Overview - Blood Donation Web Application

This web application is designed to simplify blood donation by directly connecting donors and requester without intermediaries. All users register under a single system, where they can act as both donors and requester. Once registered, users needing blood can submit a request, while donors simply wait to receive notifications about nearby requests.

The goal is to make the donation process faster and more efficient, reducing the time involved in finding a suitable donor. The platform prioritizes simplicity, ensuring a user-friendly experience with minimal steps.

>[!IMPORTANT]
>Ensure mysql docker container running before running this web application.
### Prerequisites
Ensure the latest version of python3 and pip are installed. [Python3 Download](https://www.python.org/downloads/) Ensure to download the right version on your system.

Ensure Docker installed, please follow the instructions from here: [Windows](https://docs.docker.com/desktop/setup/install/windows-install/) For [MacOS](https://docs.docker.com/desktop/setup/install/mac-install/)

Clone the repository

```bash
git@github.com:CAA900-PRIME/blooddonation-backend.git
```
#### Environment Setup
Before starting the web application, must first initialize python environment using:

```bash
python3 -m venv env
```

>[!NOTE]
>Python **environment**: to make it simple, its just a safe place were all the required packages of the web application are installed safely and are not conflicted with the system host.

And to activate the environment: 

```bash
source env/bin/activate
```

>[!IMPORTANT]
>To exit out of the environment, must enter keyword `deactivate` from within the activated shell. Then it will get out of that environment.

### Start

Before starting the application, there are packages must be installed first. All the required packages are defined within a file called `requirements.txt`. To install these package, execute the following command.

```bash
pip install -r requirements.txt
```

**NOTE**: ensure the current directory, must contain the file `requirements.txt`

To start the application 

```bash
python3 app.py
```

>[!NOTE]
>If there are any new libraries you have included to this project in the future, don't forget to execute `pip freeze > requirements.txt` to update list in that file.
### Project Requirements and Features

- [x] Full Functional Authentication | Login & Sign Up Pages (Done)
- [x] Filling out blood request application for each user
### API Requests
Getting available events, this is only for testing the requests
```bash
curl localhost:3000/api/events/get-events
[{"date":"2025-02-10","name":"City Hospital Blood Drive"},{"date":"2025-02-15","name":"Community Center Donation Day"},{"date":"2025-02-20","name":"University Blood Donation Camp"}]
```

##### Getting list of signed up users, this is only for testing. We might need this to be available for admin or staff users.

Get all users (This only works for testing)
```bash
curl localhost:3000/api/users/get-users  
[{"Date Of Birth":"Mon, 01 Jan 1990 00:00:00 GMT","createdDate":"Fri, 21 Feb 2025 20:26:41 GMT","email":"omarali@example.com","firstName":"Omar","id":1,"lastLoggedIn":null,"lastName":"Ali","phone_number":"1234567890","postalCode":"A1A 1A1","username":"OmarAli","verifiedDate":null}]
```

POST: User sign up successfully. 
```bash
curl -X POST http://localhost:3000/api/auth/signup \
     -H "Content-Type: application/json" \
     -d '{
           "username": "OmarAli",
           "password": "@Password",
           "email": "omarali@example.com",
           "phone_number": "1234567890",
           "firstName": "Omar",
           "lastName": "Ali",
           "dob": "1990-01-01",
           "postalCode": "A1A 1A1"
         }'
     {"message":"Signup successful! Please login."}
```

POST: User login successfully.
```bash
curl -X POST http://localhost:3000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{
           "username": "OmarAli",
           "password": "@Password"
         }'

    {"message":"Logged in successfully","username":"OmarAli"}
```

#### Getting all the countries and cities as well as cities based on country code

Get all countries
```bash
curl localhost:3000/api/country/get-countries
{"countries":[{"code":"CA","id":1,"name":"Canada"},{"code":"US","id":2,"name":"United States"}]}
```

Get all cities
```bash
curl localhost:3000/api/city/get-cities
{"cities":[{"id":1,"name":"Toronto"},{"id":2,"name":"Vancouver"},{"id":3,"name":"Montreal"},{"id":4,"name":"Calgary"},{"id":5,"name":"Edmonton"},{"id":6,"name":"Ottawa"},{"id":7,"name":"Winnipeg"},{"id":8,"name":"Quebec City"},{"id":9,"name":"Halifax"},{"id":10,"name":"Saskatoon"},{"id":11,"name":"New York"},{"id":12,"name":"Los Angeles"},{"id":13,"name":"Chicago"},{"id":14,"name":"Houston"},{"id":15,"name":"Phoenix"},{"id":16,"name":"Philadelphia"},{"id":17,"name":"San Antonio"},{"id":18,"name":"San Diego"},{"id":19,"name":"Dallas"},{"id":20,"name":"San Jose"}]}
```

Get all cities based on country code
```bash
curl localhost:3000/api/city/get-cities-with-code/US
{"cities":[{"id":11,"name":"New York"},{"id":12,"name":"Los Angeles"},{"id":13,"name":"Chicago"},{"id":14,"name":"Houston"},{"id":15,"name":"Phoenix"},{"id":16,"name":"Philadelphia"},{"id":17,"name":"San Antonio"},{"id":18,"name":"San Diego"},{"id":19,"name":"Dallas"},{"id":20,"name":"San Jose"}]}

curl localhost:3000/api/city/get-cities-with-code/CA
{"cities":[{"id":1,"name":"Toronto"},{"id":2,"name":"Vancouver"},{"id":3,"name":"Montreal"},{"id":4,"name":"Calgary"},{"id":5,"name":"Edmonton"},{"id":6,"name":"Ottawa"},{"id":7,"name":"Winnipeg"},{"id":8,"name":"Quebec City"},{"id":9,"name":"Halifax"},{"id":10,"name":"Saskatoon"}]}
```

## Security Features (Merged - Not Tested Yet)

>[!NOTE]
The feature has been merged to the main branch successfully, however, it has not been tested yet. The testing will be done in the coming weeks. This will cover to ensure integration with the front-end as well.

### Two-Factor Authentication (2FA) Implementation
#### Overview
This document describes the implementation of Two-Factor Authentication (2FA) in the Blood Donation Web App backend.

#### Changes Made

**1. Database Changes**
- **Added `otp_secret` column** to `Users` model (`models/user.py`) to store the OTP secret key.

**2. New Model for OTP Handling**
- Created `models/two_factor.py` for OTP generation and verification.

**3. API Endpoints for 2FA (`api/user.py`)**
- **Enable 2FA:** `/enable-2fa` (Stores OTP secret for user)
- **Generate OTP:** `/generate-otp` (Generates OTP using stored secret)
- **Verify OTP:** `/verify-otp` (Validates the OTP entered by the user)

#### How to Test
1. Enable 2FA for a user:
```json
POST /enable-2fa
{
 "user_id": 1
}
```

### Issues
If you encounter any issues, please create a new issue on GitHub or Jira. Describe the problem in detail, and feel free to assign it to yourself or someone else if you plan to fix it.
