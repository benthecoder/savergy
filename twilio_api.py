# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import streamlit as st

account_sid = st.secrets["account_sid"]
auth_token = st.secrets["auth_token"]

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = "account_sid_key"
# auth_token = "auth_token"


def send_message(phone_num: str, message: str):

    client = Client(account_sid, auth_token)

    message = client.messages.create(body=message, from_="+12626864433", to=phone_num)
