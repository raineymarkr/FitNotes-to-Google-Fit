import csv
import datetime
import time
import uuid
import json
import os
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Constants
CLIENT_SECRET_FILE = r'SECRET_FILE'
SCOPES = ['https://www.googleapis.com/auth/fitness.activity.write']

def get_credentials():
    creds = None

    # Load the WCc JSON and adjust the keys
    with open(CLIENT_SECRET_FILE, 'r') as file:
        data = json.load(file)
        wc_data = data["WCc"]
        client_config = {
            "installed": {
                "client_id": wc_data["client_id"],
                "project_id": wc_data["project_id"],
                "auth_uri": wc_data["Anc"],
                "token_uri": wc_data["hVc"],
                "auth_provider_x509_cert_url": wc_data["znc"],
                "client_secret": wc_data["s2a"],
                "redirect_uris": wc_data["oNc"]
            }
        }

    if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def datetime_to_milliseconds(date):
    split = date.split("-")
    dt = datetime.datetime(int(split[0]), int(split[1]), int(split[2]), 11, 00, 00)
    epoch_seconds = (dt - datetime.datetime(1970,1,1)).total_seconds()

    return int(epoch_seconds*1000)

workouts = []

if len(sys.argv) < 2:
    print("Please provide the data file as an argument.")
    sys.exit(1)

data_file = sys.argv[1]

with open(data_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    lastdt = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            ntime = datetime_to_milliseconds(row[0])
            if ntime > lastdt:
                data = {
                    "id": str(uuid.uuid4()),
                    "name": "workout",
                    "description": "workout time",
                    "startTimeMillis": datetime_to_milliseconds(row[0]),
                    "endTimeMillis": datetime_to_milliseconds(row[0])+3600000,
                    "modifiedTimeMillis": datetime_to_milliseconds(row[0]),
                    "activityType": 97,
                    "activeTimeMillis": 3600000,
                    }
                workouts.append(data)
                line_count += 1
                lastdt = ntime
def upload_workout(data_array):
    creds = get_credentials()
    service = build('fitness', 'v1', credentials=creds)
    requests_made = 0
    for session in data_array:
        # Insert session
        service.users().sessions().update(userId='me', sessionId=session['id'], body=session).execute()
        print(f'Added {session["startTimeMillis"]}')
        requests_made += 1
        if requests_made % 500 == 0:  # Every 500 requests
            time.sleep(60)  # Wait for 10 minutes (600 seconds)
        else:
            time.sleep(1)  # Otherwise, wait for 1 second between requests
    
    
upload_workout(workouts)