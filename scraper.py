from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import errors
import requests
import base64
import email
import datetime
from io import StringIO

class MailItem():
    def __init__(self, id, message):
        self.id = id
        self.message = message


class SorteoTable():
    def __init__(self):
        self.sorteo2 = ""
        self.sorteo4 = ""
        self.sorteo5 = ""


def getMessages(service, user_id, query= ''):
    response = service.users().messages().list(userId=user_id,q=query).execute()
    messages = []

    now = datetime.datetime.now()

    for message in response['messages']:

        response = service.users().messages().get(userId=user_id, id=message['id'],format='raw').execute()
        msg_str = base64.urlsafe_b64decode(response['raw'].encode('ASCII'))

        day_str = ", " + str((now.day - 1))

        if not day_str.encode() in msg_str:
            messages.append(MailItem(message['id'],msg_str))


    return messages

def messagesFilter(sorteo_table,stored_messages):

    for messages in stored_messages:
        print(messages.id)

        if b"sorteo:2" in messages.message:
            print('success sorteo 2')
            sorteo_table.sorteo2 = messages.message

        if b"sorteo:4" in messages.message:
            print('success sorteo 4')
            sorteo_table.sorteo4 = messages.message

        if b"sorteo:5" in messages.message:
            print('success sorteo 5')
            sorteo_table.sorteo5 = messages.message


def sorteosFilter(sorteo_table):

    decoded_str = sorteo_table.sorteo2.decode("utf-8")

    sorteo_list_str = decoded_str.split("(190.112.211.242)",1)[1]

    i = 0;
    sio = StringIO(sorteo_list_str)
    for sline in sio.readlines():

        rules = [i != 0,i != 1,i != 15,i != 16]

        if all(rules):

            print(sline)

        i += 1


SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('credentials.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)

service = build('gmail', 'v1', http=creds.authorize(Http()))
current_date = datetime.datetime.today().strftime('%Y-%m-%d')
stored_messages = getMessages(service,'me','from:webmaster@tedepasa.com after:' + current_date)
sorteo_table = SorteoTable()

messagesFilter(sorteo_table,stored_messages)

sorteosFilter(sorteo_table)
