"""Main program for Microsoft Graph Connect sample.
To run the app, execute the command "python manage.py runserver" and then
open a browser and go to http://localhost:5000/
"""
import flask_script
import application

MANAGER = flask_script.Manager(application.app)
MANAGER.add_command('runserver', flask_script.Server(host='roommonitor.heroku.com'))
MANAGER.run()
