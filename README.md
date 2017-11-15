Amazon Echo Teamproject
=======================
This repository contains two different Alexa Custom skills.
1. Room Monitor
2. Predictive Maintanance for Solar panels

Both skills can be independently run Alexa. For further instruction see below. More information can be found in other READMEs in this repository.


## How to run the skill
### Prerequisites 
* Amazon Developer Account
* Microsoft Account (Room monitor)
* Microsoft Application (Room monitor)

The skills are deployed on different servers, Amazon Lambda for Room Monitor and Heroku for the predictive maintainance.
The app can be tested either online over the Amazon developer console or on a raspberry pi with Alexa installed or on an actual Alexa.


### Room monitor
The room monitor skill can book rooms and check their availability. Rooms are represented as Outlook calendars, so a valid Outlook Account must be present
as well an account linking which has to be done by creating a Microsoft Application.
Additionally a dashboard is provided to manage the rooms with are registered for the room monitor. Here rooms can be added, removed and events be seen.
The Dashboard can be found [here](https://ghk3pcg5q0.execute-api.us-east-1.amazonaws.com/dev).

### Predictive maintainance 
Here you can get very precise information about the power generation of solar panels.


