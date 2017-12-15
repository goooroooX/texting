#!/usr/bin/python
# -*- coding: utf-8 -*-
#################################################
#                twillio SMS messages           #
#            author: Dmitry Nikolaenya          #
#            https://github.com/goooroooX       #
#               https://gooorooo.com            #
#################################################

# Copyright 2017 Dmitry Nikolaenya
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# NOTE: does not work with Python 2.6!

# chmod +x /opt/texting/texting.py
# ln -s /opt/texting/texting.py /opt/texting/texting

VERSION = "1.1"
RELEASE = "20171013"
NOTES = """
20171013: WIN* removal for twilio (SMS with this text blocked).
"""
import os, sys
import traceback
import logging
from logging.handlers import RotatingFileHandler
import re

PHONE_NUMBERS = [
    '+12322222222'
    ]

FROM   = "+12311111111"
SID    = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
TOKEN  = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
FIXED  = "MESSAGE HEADER"

if getattr(sys, 'frozen', False):
    root_folder = os.path.dirname(os.path.abspath(sys.executable))
else:
    root_folder = os.path.dirname(os.path.abspath(__file__))

libs_folder = os.path.join(root_folder, 'lib')
sys.path.append(libs_folder)
if os.path.isdir(libs_folder):
    sys.path.append(libs_folder)
    for zipped in os.listdir(libs_folder):
        extension = os.path.splitext(zipped)[1]
        if extension in [".egg", ".whl", ".zip"]:
            sys.path.append('%s/%s' % (libs_folder, zipped))

def my_logger(LOG_FILENAME):
    FORMAT_FILE = '%(asctime)-15s %(levelname)-8s : %(message)s'
    FORMAT_CLI  = '%(asctime)-8s %(levelname)-8s %(message)s'
    MAX_BYTES = 3*1024*1024
    BACKUP_COUNT = 10
    logger = logging.getLogger()
    # logging to file only
    fileFormatter = logging.Formatter(FORMAT_FILE)
    fileHandler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(fileFormatter)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.DEBUG)
    return logger

LOG_NAME = os.path.join("/var/log", "alert_texting.log")
log = my_logger(os.path.join(root_folder, LOG_NAME))
log.info("Initializing...")

if len(sys.argv) < 2:
    log.error("Please provide message text as argument(s)!")
    sys.exit(1)

cert_folder = os.path.join(root_folder, 'cert')
cert = os.path.join(cert_folder, "cacert.pem")
if not os.path.isfile(cert):
    log.error("Twillio certificate not found: %s" % cert)
    sys.exit(1)

# NOTE: twilio should be unpacked to get cacert.pem from 'twilio/conf' folder
# ca_cert_path = os.path.join(current_path, '..', '..', 'conf', 'cacert.pem')
# but we can monkey-patch twilio.http initialization
def get_cert_file_mod():
    return os.path.abspath(cert)

import twilio
from twilio.http import get_cert_file
twilio.http.get_cert_file = get_cert_file_mod
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client(SID, TOKEN)

MESSAGE = FIXED

# process other CLI arguments
log.info("MESSAGES:")
for text in sys.argv[1:]:
    log.info("  > %s" % text)
    MESSAGE = MESSAGE + "\n" + text

MESSAGE = MESSAGE.decode('string_escape')
# need to get rid of all WIN* words, twilio does not like them
MESSAGE = re.sub("(wins*?)\s", "*** ", MESSAGE, flags=re.IGNORECASE)
log.debug("FINAL MESSAGE: %s" % MESSAGE)

for number in PHONE_NUMBERS:
    log.info(" > sending to: %s" % number)
    try:
        message = client.messages.create(to=number, from_=FROM, body=MESSAGE)
        log.info("  > OK:")
        log.info("   >> sid:   %s" % message.sid)
        log.info("   >> price: %s" % message.price)
    except TwilioRestException as e:
        log.error("  > TWILIO exception:")
        log.error("   >> error:  %s" % e.msg)
        log.error("   >> code:   %s" % e.code)
        log.error("   >> status: %s" % e.status)
        continue
    except:
        log.error("  > UNHANDLED exception:")
        log.error("   >> %s" % traceback.format_exc())
        continue
log.info("Finalized...")

#EOF