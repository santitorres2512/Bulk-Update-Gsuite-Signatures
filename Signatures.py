from __future__ import print_function        #imports special print function for HTML formats

from apiclient import discovery              #Gmail API import
from httplib2 import Http
from oauth2client import file, client, tools   #OAuth2 protocol import for client crendentials


#Data is the signature's body, which is HTML format
DATA= {'signature': '<p><img src="https://f.hubspotusercontent40.net/hubfs/1709048/Banner-CT-Newsletter-08.jpg" alt="" /></p><p>&nbsp;</p><p><a href="https://www.cloudtask.com/privacy-policy">Privacy Policy &amp; Terms of Use</a></p>'}
#Scope (permission set) aimed by the API 
SCOPES = 'https://www.googleapis.com/auth/gmail.settings.basic'
#Json file where the script logs are temporarily saved
store = file.Storage('storage.json')
creds = store.get()                                                             #authentication stage
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json',SCOPES)          #import the client credentials
    creds = tools.run_flow(flow,store)                                          #and authenticate using v1 API
GMAIL = discovery.build('gmail','v1',http=creds.authorize(Http()))
    
addresses = GMAIL.users().settings().sendAs().list(userId='ttest@cloudtask.com', #Authenticated under this userid
fields='sendAs(isPrimary,sendAsEmail)').execute().get('sendAs', [])              #for applying the actions 
for address in addresses:
    if address['isPrimary']:
        break
        
rsp = GMAIL.users().settings().sendAs().patch(userId='me',                      #to these user ids, 'me' is just a testing variable
                                              
sendAsEmail=address['sendAsEmail'],body=DATA).execute()                         #just replace me for the gmail username of the employee to update
print("Primary address changed to:", rsp['signature'])

#BELOW IS AN ALTERNATE VERSION OF THIS SCRIPT

'''

Create creds from helpdesk
research about getting all user Ids under a team


primary_alias = None
aliases = gmail_service.users().settings().sendAs().\
    list(userId='me').execute()
for alias in aliases.get('sendAs'):
    if alias.get('isPrimary'):
        primary_alias = alias
        break

sendAsConfiguration = {
    'signature': 'I heart cats'
}
result = gmail_service.users().settings().sendAs().\
    patch(userId='me',
          sendAsEmail=primary_alias.get('sendAsEmail'),
          body=sendAsConfiguration).execute()
print 'Updated signature for: %s' % result.get('displayName')


primary_alias = None
aliases = gmail_service.users().settings().sendAs().\
    list(userId='me').execute()
for alias in aliases.get('sendAs'):
    if alias.get('isPrimary'):
        primary_alias = alias
        break

sendAsConfiguration = {
    'signature': 'I heart cats'
}
result = gmail_service.users().settings().sendAs().\
    patch(userId='me',
          sendAsEmail=primary_alias.get('sendAsEmail'),
          body=sendAsConfiguration).execute()
print 'Updated signature for: %s' % result.get('displayName')
primary_alias = None
aliases = gmail_service.users().settings().sendAs().\
    list(userId='me').execute()
for alias in aliases.get('sendAs'):
    if alias.get('isPrimary'):
        primary_alias = alias
        break

'''