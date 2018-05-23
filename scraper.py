from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import errors
import requests
import base64
import email
import datetime

class MailItem():

    def __init__(self, id, message):
        self.id = id
        self.message = message

def getMessages(service, user_id, query= ''):
    response = service.users().messages().list(userId=user_id,q=query).execute()
    messages = []

    for message in response['messages']:

        response = service.users().messages().get(userId=user_id, id=message['id'],format='raw').execute()
        msg_str = base64.urlsafe_b64decode(response['raw'].encode('ASCII'))
        messages.append(MailItem(message['id'],msg_str))

    return messages


def messagesFilter(stored_messages):

    for messages in stored_messages:
        print(messages.id)



SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('credentials.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)

service = build('gmail', 'v1', http=creds.authorize(Http()))
current_date = datetime.datetime.today().strftime('%Y-%m-%d')
stored_messages = getMessages(service,'me','from:webmaster@tedepasa.com after:' + current_date)
messagesFilter(stored_messages)
