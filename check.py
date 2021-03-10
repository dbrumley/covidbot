#!/usr/bin/env python3

# Bot to check local rite-aids, identified by store number, for
# covid vaccine appointments.  The bot polls the rite-aid API
# every 10 seconds.  It texts you when an appointment is available.
# The list of store ID's is below; you can go to $register_url
# below and search by your zip code to find store ID's near you.
# By default it's the list of stores within 10 miles of CMU.
#
# This requires a twilio.com account. They are free.
#
# To install:
#   $ pip install twilio
#
# To use:
#   NOTE: ALL PHONE NUMBERS ARE OF THE FORM "+14125551212"
#   You need to include the "+1" and have the full 7 digits
#   $ export TWILIO_ACCOUNT_SID = <your SID>
#   $ export TWILIO_AUTH_TOKEN = <your token>
#   $ export TWILIO_PHONE = <your twilio phone number> (from text #)
#   $ export CELLPHONE = <your cell phone> (to text #)
#   $ ./check.py
#   <you can also hard code the above in the variables below>

import requests
from twilio.rest import Client
import os
import time
from datetime import datetime, timedelta

# The main rite-aid page for covid in PA.
register_url = "https://www.riteaid.com/pharmacy/covid-qualifier"

# I got this list of rite-aid store IDs manually from register_url.
stores_near_me = [4682, 10934, 10954, 1370, 3527, 1925, 10919, 10914]

# Your cell phone. This is the "to" we text to.
to_phone = os.environ['CELLPHONE']

# The twilio-assigned phone number for texting. This will be the "from"
# address when you receive a text.
from_phone = os.environ['TWILIO_PHONE']

# Twilio information from your account. 
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

# Don't re-text about a store with appts within this time interval.
text_interval = timedelta(minutes=15)

# Key is a store ID, value is the next it's ok to text.
# Used to make sure we don't text about the same store having appts
# every time we poll (every 10 seconds).
riteaid = dict.fromkeys(stores_near_me, datetime.now())

# rite-aid API server; swiped from register_url originally.
baseurl = "https://www.riteaid.com/services/ext/v2/vaccine/checkSlots?storeNumber="

client = Client(account_sid, auth_token)

def text_like_a_teen(r):
    client.messages.create(
        to=to_phone,
        from_=from_phone,
        body="COVID Appointments available at store {}. Go to {} to grab it!".format(r, register_url))


def check_availability():
    for r in dict.keys(riteaid):
        url = baseurl + str(r)
        print("Checking: {}".format(url))
        res = requests.get(url).json()
        if res['Status'] == 'ERROR':
            continue
        slots = res['Data']['slots']
        if slots['1'] is True or slots['2'] is True:
            now = datetime.now()
            print("COVID Slots available {}".format(url))

            # Text if we're outside the "no re-text" interval
            if now >= riteaid[r]:
                text_like_a_teen(r)
                # Don't text again until text_interval has elapsed!
                riteaid[r] = now+text_interval


while (True):
    slots_available = check_availability()
    # Poll every 120 seconds. Why 120? Why not! 
    # Seriously, though, don't change this to below, say, 10.
    # We don't want to over-tax rite-aid servers.
    time.sleep(120)
