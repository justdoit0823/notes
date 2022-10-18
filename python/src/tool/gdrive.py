from __future__ import print_function
from fileinput import filename

import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


GOOGLE_AUTH_CREDENTIAL = "GOOGLE_AUTH_CREDENTIAL"

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive'
]

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
DEFAULT_MIME_TYPE = 'application/octet-stream'
MIME_TYPES = {
    'gz': 'application/gzip',
    'gif': 'image/gif',
    'htm': 'text/html',
    'html': 'text/html',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'js': 'text/javascript',
    'json': 'application/json',
    'png': 'image/png',
    'pdf': 'application/pdf',
    'ppt': 'application/vnd.ms-powerpoint',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'sh': 'application/x-sh',
    'svg': 'image/svg+xml',
    'tar': 'application/x-tar',
    'tif': 'image/tiff',
    'tiff': 'image/tiff',
    'txt': 'text/plain',
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'xml': 'application/xml',
    'zip': 'application/zip'
}

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    credential_file = os.environ.get(GOOGLE_AUTH_CREDENTIAL, 'credentials.json')
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credential_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def upload_file(filepath, mimetype, resumable=False):
    """Insert new file.
    Returns : Id's of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    filename = os.path.basename(filepath)
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=get_credentials())

        file_metadata = {'name': filename}
        media = MediaFileUpload(filepath, mimetype=mimetype, resumable=resumable)
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(F'File ID: {file.get("id")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')

def list_files():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    try:
        service = build('drive', 'v3', credentials=get_credentials())

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

def upload():
    if len(sys.argv) < 4:
        raise Exception("missing parameters")

    filepath = sys.argv[2]
    mimetype = sys.argv[3]
    upload_file(filepath, mimetype)

def sync_files():
    if len(sys.argv) < 3:
        raise Exception("missing parameters")
    
    upload_cnt = 0
    file_id = None
    for root, dirs, files in os.walk(sys.argv[2]):
        for filename in files:
            filepath = os.path.join(root, filename)

            parts = filename.split(".")
            mime_type = None
            if len(parts) == 1:
                mime_type = DEFAULT_MIME_TYPE
            else:
                mime_type = MIME_TYPES.get(parts[1].lower(), DEFAULT_MIME_TYPE)
            
            filesize = os.path.getsize(filepath)
            if filesize > 5 * 1024 * 1024:
                file_id = upload_file(filepath, mime_type, resumable=True)
            else:
                file_id = upload_file(filepath, mime_type)

            print(f'{filename} file id {file_id}')
            upload_cnt += 1
    
    print(f'uploaded {upload_cnt} files.')


def main():
    cmd = sys.argv[1]
    if cmd == "list":
        list_files()
    elif cmd == 'upload':
        upload_file()
    elif cmd == 'sync':
        sync_files()
    else:
        print('unsupported command')


if __name__ == '__main__':
    main()