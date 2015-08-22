__author__ = 'jakeway'

""" This file contains methods to send text messages via Twilio"""

from app import app
from twilio.rest import TwilioRestClient


TWILIO_SID = app.config['TWILIO_SID']
TWILIO_TOKEN = app.config['TWILIO_TOKEN']


def send_alert(bus_name, bus_stop, eta, phone_number, event):
    client = TwilioRestClient(TWILIO_SID, TWILIO_TOKEN)
    text = 'The ' + bus_name + ' is arriving at ' + bus_stop + ' in ' + str(eta) + ' minutes.'
    text = text + " Don't miss it or you will be late to " + event + '!'
    message = client.messages.create(body=text, to=phone_number, from_=+17329933336)
    print message.sid