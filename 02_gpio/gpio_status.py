from flask import Flask
from flask_ask import Ask, statement, convert_errors
import RPi.GPIO as GPIO
import logging

GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger("flask_ask").setLevel(logging.DEBUG)
@ask.launch
def invoke():
    # welcome_msg = render_template('welcome')
    return question('What status do you want to know')
@ask.intent('GPIOControlIntent', mapping={'pin': 'pin'})
def status_check(pin):
	try:
	    pinNum = int(pin)
	except Exception as e:
	    return statement('Pin number not valid.')
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pinNum, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	status = GPIO.input(pinNum)
	#GPIO.add_event_detect(pinNum, GPIO.RISING)
	return statement('Meeting room status of room {} is {}'.format(pinNum, status))
@ask.intent('GPIOAllStatusIntent'):
def check_all():
	try:
	#call func in loop
	except Exception as e:
		return statement('Pin number not connecte')
	return statement('add list o status of all pins')

if __name__ == '__main__':
    app.run(debug=True)	
