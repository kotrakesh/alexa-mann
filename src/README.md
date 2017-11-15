Amazon Echo Room Monitor
=======================

## Project Purpose 
This project enables users to book meeting rooms in a company environment with the help of Alexa as a voice interface for a hands free room booking experience.
Possible (implemented) use cases are:
* Booking a meeting room with the information about, date, time, duration, number of attendees and title of the event
* Checking availability of specific rooms for specific dates and times
* Overview over all registered rooms

Rooms can be managed over a Web Interface (added, deleted)


## Technical Prerequisites
There are some prerequisites that must be fulfilled in order to be able to run the program.
* Microsoft Outlook Account
* Amazon Developer Account
* Amazon Lambda Account
* Python3 and Git have to be installed
* internet connectivity has to be available throughout the whole process 


## File Structure

```
src
+---static
|      +---script.js
|      +---style.css
+---templates
|     +---main.html
|     +---header.html
|     +---events.html
+---app.py
+---util.py
+---ms-endpoints.py
+---room_class.py
+---templates.yaml
+---requirements.txt
+---zappa_settings.json
```

### Shared
* app.py  Contains the logic
* util.py Contains utility functions used by Amazon and MS Graph

### Amazon Alexa
* room_class.py Stores the values given by the user during the room booking process
* templates.yaml Sentences Alexa will say

### Microsoft Graph
* ms_endpoints.py Endpoints to the MS Graph API
* templates/ HTML pages for the webfrontend 
* static/ Folder for static files like CSS or Javascript files

### Misc
* zappa_settings.json Deployment settings for Amazon Lambda
* requirements.txt python packages needed, install with pip install -r requirements.txt


## Setup the Project 
This project can either be run locally or can be deployed on Amazon Lambda. 
The local mode is covered in a extra README file.
To deploy it on Amazon Lambda the following guide covers all necessary steps.

[Deploy on Amazon Lambda with zappa](https://developer.amazon.com/de/blogs/post/8e8ad73a-99e9-4c0f-a7b3-60f92287b0bf/new-alexa-tutorial-deploy-flask-ask-skills-to-aws-lambda-with-zappa)

Note: As the repository already contains a zappa_settings file, the initialization of the zappa configuration is not needed.
All what is left is simply to deploy the skill by typing:

```
zappa deploy dev
```
 
The initial deployment process can take a few minutes while Zappa creates API gateways and bundles and uploads the code and dependencies. Releasing code updates doesn't recreate the API gateways and is a bit faster. 

If file in the repository changes the updates are handled through a separate command:
```
zappa update dev
```

After deploying or updating, Zappa outputs the URL your skill is hosted at. The URL looks similar to this one:
https://mcgalgvft5.execute-api.us-east-1.amazonaws.com/dev



## How to run the skill?
Once everything is uploaded and deployed on Lambda the custom skill can be tested either over the Amazon Developer Console, a raspberry pi or on a real Alexa.

### Possible invocation calls for the custom skill:
* ```launch room monitor```
* ```tell room monitor to book me a room tomorrow```
* ```ask room monitor if room number 1 is available```
* ```ask room monitor which rooms can I book```

These call can be adapted and fed with more information like the date and time when the meeting should be scheduled. If this is not given in the beginning, Alexa will ask for all missing information it needs to book a room.

### Amazon Developer Console
Go to __Test__ Tab in the amazon developer console and start the testing with the *Invocation Name* specified at the __Skill Information__ Tab (room monitor)
![Test Skill](/doc/alexa_test.png)

### Raspberry PI
Please follow the official guide of Amazon to set up the raspberry pi as an Alexa.
[Link to guide](https://github.com/alexa/alexa-avs-sample-app/wiki/Raspberry-Pi)

### Alexa Echo, Dot, ...
Connect the Alexa to the Amazon User account via the mobile app. This will take a few minutes and each required step will be displayed on the mobile app. 
Once Alexa is connected you can start the custom skill by saying: ```Alexa```

Note, that only after the ring flashed Alexa is ready for further commands and the custom skill can be invoked by saying 
```start room monitor```
Each function can also be called directly without invoking the Launch Request. Please refer to the possibilities mentioned in the beginning.


## Common Problems
- Alexa will discard the security token of the MS Graph API every once in a while. Once this happens, the skill has to be reconnected (linked) again to the MS Account.
- For the title of the event the built-in datatype "Literal" is used. In a few cases, especially when keywords like dates or numbers are used as a title, Alexa will mistake them as a request to a different intent and thus Alexa might ask for information twice and go into a loop. Therefore only titles which are unique and can't be mistaken as any other built-in datatype may be used


## Implementation Details

### General Structure and Implementation Documentation








