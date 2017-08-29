
@app.route('/')
def index():
    """Handler for home page."""
    return login()

import json
import sys
import uuid
import logging
import requests

from flask     import Flask, redirect, url_for, session, request, render_template

#Custom

#from durationparser import getMeetingEndTime
#from room_class import Room
#from alexa_custom_skill import *
from ms_graph_endpoint import call_createvent_endpoint, call_listevents_for_time_endpoint, call_createcalendar_endpoint, call_deletecalendar_endpoint
from utilities import convert_amazon_to_ms, get_infor_from_alexa, create_room_to_json


room = Room()




# https://forums.developer.amazon.com/questions/5428/how-to-link-an-amazon-alexa-skill-using-azure-app.html
# http://www.macadamian.com/2016/03/24/creating-a-new-alexa-skill/

from package_msgraph import app
