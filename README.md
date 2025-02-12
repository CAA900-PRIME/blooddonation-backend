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
###### Here will define all requirements and feature our web application:

- [x] Full Functional Authentication | Login & Sign Up Pages
### Issues
If you encounter any issues, please create a new issue on GitHub or Jira. Describe the problem in detail, and feel free to assign it to yourself or someone else if you plan to fix it.
