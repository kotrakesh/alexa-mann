# Installing and running a sample Alexa Skill (Development)
This short tutorial provides a quick overview of how to run an Alexa custom skill in the development mode. Changes can be applied quickly and also tested via the Amazon Developer Console.

## Prerequisites 
* python
* git 
* flask-server
* flask-ask
* ngrok
* Amazon Developer Account


## Start Amazon Sample App

On __Linux__

1. run `./ngrok http 5000`

On __Windows__

1. run `ngrox.exe http 5000`

2. create sample app at [developer.amazon.com](developer.amazon.com)
3. specify __Skill Information__ and save configuration
![Skill Information](alexa_skill-information.png)
4. Fill out __Interaction Model__ (*Intent Schema* and *Sample Utterances*)
5. copy the https Link displayed by ngrok and insert it at the __Configuration__ Tab (Endpoint)
![Configuration](alexa_configuration.png)
6. Select the __SSL-Certificate__
![SSL-Certificate](alexa_ssl-certificate.png)
7. run `python sample.py`
8. Go to __Test__ Tab in the amazon developer console and start the testing with the *Invocation Name* specified at the __Skill Information__ Tab
![Test Skill](alexa_test.png)

