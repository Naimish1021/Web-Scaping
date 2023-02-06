import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient import discovery
import json
import time

CLIENT_SECRET = 'client_secret.json'
SCOPE = 'https://www.googleapis.com/auth/blogger'
STORAGE = Storage('credentials.storage')
# Start the OAuth flow to retrieve credentials
def authorize_credentials():
# Fetch credentials from storage
    credentials = STORAGE.get()
# If the credentials doesn't exist in the storage location then run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials
credentials = authorize_credentials()
print(credentials)
credentials = authorize_credentials()
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://blogger.googleapis.com/$discovery/rest?version=v3')
service = discovery.build('blogger', 'v3', http=http, discoveryServiceUrl=discoveryUrl,developerKey='AIzaSyAhUizeWSI8rTdUaiUqlVul-A4Z-x29AQQ') 
users = service.users()
# Retrieve this user's profile information
thisuser = users.get(userId='self').execute()
print('This user\'s display name is: %s' % thisuser['displayName'])
page=service.pages()

def post_data(data):
    global page

    for item in data:
        payload={
        "title":f'question: {item["question"]}',
        "content": f"<h1> question: {item['question']}</h1> <br><p> ansewer: {item['answer'][0]} </p>",
        }
        respost=page.insert(blogId='621232213779134592',body=payload,isDraft=True).execute() #publishing the new post
        print(" page id:",respost['id'])
        
data  = json.load(open('new 27.json'))
end = len(data['data'])-(len(data['data'])%5)
for i in range(0,end,5):
    post_data(data['data'][i:i+5])
    time.sleep(60)