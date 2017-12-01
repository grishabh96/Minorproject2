import json
from random import choice

import os

import requests
from flask import Flask, request

import config
import modules
from templates.quick_replies import add_quick_reply
from templates.text import TextTemplate
import smtplib


def process(mailto,input):
    output = {}
    try:
       
        gmailaddress = "grishabh74@gmail.com"
        gmailpassword ="21081996"
        x=input.split(' ')
        
        msg=x[2:]
        msg = ''.join([i for i in msg ])
        mailServer = smtplib.SMTP('smtp.gmail.com' , 587)
        mailServer.starttls()
        mailServer.login(gmailaddress , gmailpassword)
        mailServer.sendmail(gmailaddress, mailto , msg)
        mailServer.quit()

       
    except:
        output['success'] = False
    return output



    
