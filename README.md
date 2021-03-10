# COVID Pennsylvania Appointment Bot

This is a bot that polls rite-aids for available COVID appointments, and will
text you when they become available. I wrote this because as an active cancer
patient, I am a member of 1a for [Pennsylvania's vaccine roll
out](https://www.health.pa.gov/topics/disease/coronavirus/Vaccine/Pages/Vaccine.aspx),
but found it incredibly difficult to get an appointment.

I am unable to support this. I went back and forth on whether to release at all,
but ultimately decided based upon interest from [twitter
interest](https://twitter.com/thedavidbrumley). I also didn't feel right about
putting myself in a spot to decide who had an advantage getting a spot and who
did not. The bot itself is quite trivial, and illustrates how easily PA could
have incorporated something similar itself.



## How it works

You need to know how to install python, edit small python programs, and run
programs from the command line. The code is pretty simple: it checks a list of
rite-aids, identified by store number, for COVID vaccine appointments. It texts
you when an appointment is available.  The code is hopefully over-commented so
it is clear where to change things. 

Before running, please edit the list of stores (`stores_near_me` in the code)
with those actually close to you.  You can find stores with the vaccine in PA by
going to [https://www.riteaid.com/pharmacy/covid-qualifier].


This requires a [twilio.com](https://twilio.com) account. They are free.

To install:
```
  $ pip install twilio
```

To use:
  NOTE: ALL PHONE NUMBERS ARE OF THE FORM "+14125551212"
  You need to include the "+1" and have the full 7 digits

```
  $ export TWILIO_ACCOUNT_SID = <your SID>
  $ export TWILIO_AUTH_TOKEN = <your token>
  $ export TWILIO_PHONE = <your twilio phone number> (from text #)
  $ export CELLPHONE = <your cell phone> (to text #)
  $ ./check.py
  <you can also hard code the above in the script if you like>
```
