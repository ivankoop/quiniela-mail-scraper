"""
Shows basic usage of the Gmail API.

Lists the user's Gmail labels.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import errors
import requests
import base64
import email


# Setup the Gmail API
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))

# Call the Gmail API
#results = service.users().labels().list(userId='me').execute()
#response = service.users().messages().list(userId='me',q='').execute()

query = 'webmaster@tedepasa.com'
user_id = 'me'



def getMessagesid(service, user_id, query= ''):
    response = service.users().messages().list(userId=user_id,q='').execute()
    messages = []

    print(query)

    if 'messages' in response:
        messages.extend(response['messages'])

    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId=user_id, q=query,pageToken=page_token, includeSpamTrash=1, maxResults=2000).execute()
        messages.extend(response['messages'])

        return messages

print(getMessagesid(service,user_id,query))


def getMessage(service,user_id,msg_id):

    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='raw').execute()

    msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

    print(msg_str)

    #mime_msg = email.message_from_string(msg_str)

getMessage(service,user_id,'1634c807066c194d')
