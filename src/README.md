Amazon Echo Room Monitor
=======================

The room monitor custom skill for Alexa Echo manages Outlook Calenders as rooms and checks
their availability and enables the user to book rooms for specific times and dates.

Prerequesites:
* Microsoft Outlook Account



## Filestructure 
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





