Amazon Echo Predictive Maintenance
=======================

The predictive maintenance skill


Prerequisites:
* Solar panel (->connected to another raspberry pi)
* MySQL database (->hosted by heroku)
* Heroku Server (->projectname alexamannheim)
* Access to a forecast service for weather data at your solar panel location (->openweatherapi)


## Filestructure
##
* app.py  Contains the logic
* dataBaseAccess_main.py Contains connections to the database via sql queries

### Misc
* requirements.txt python packages needed, install with pip install -r requirements.txt





How to run the skill?
Once everything is uploaded and deployed on Lambda the custom skill can be tested either over the Amazon Developer Console, a raspberry pi or on a real Alexa.

Amazon Developer Console
Go to Test Tab in the amazon developer console and start the testing with the Invocation Name specified at the Skill Information Tab (room monitor) Test Skill

Raspberry PI
Please follow the official guide of Amazon to set up the raspberry pi as an Alexa. Link to guide

Alexa Echo, Dot, ...
Connect the Alexa to the Amazon User account via the mobile app. This will take a few minutes and each required step will be displayed on the mobile app. Once Alexa is connected you can start the custom skill by saying: Alexa

Note, that only after the ring flashed Alexa is ready for further commands and the custom skill can be invoked by saying start room monitor Each function can also be called directly without invoking the Launch Request. Please refer to the possibilities mentioned in the beginning.

### to finish



