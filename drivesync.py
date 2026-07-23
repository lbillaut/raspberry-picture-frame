from pathlib import Path
import shutil
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
from settings import *

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

class DriveSync:
    def __init__(self, source, destination):
        self.source_path = Path(source) # not necessary
        self.destination_path = Path(destination)
        self.drive_service = None

    def sync_local(self): # Compare source folder files and destination folder files and copy any missing files
        source_file_name_set = {file.name for file in self.source_path.iterdir() if file.is_file()}
        destination_file_name_set = {file.name for file in self.destination_path.iterdir() if file.is_file()}
        missing_files = source_file_name_set - destination_file_name_set
        for file_name in missing_files:
            file_path = self.source_path / file_name
            shutil.copy(file_path, self.destination_path)

    def sync_to_drive(self): # Compare drive folder files and destination folder files and download any missing files
        self.authenticate()
        print("Authenticated")
        missing_files = self.find_missing_files()
        for file in missing_files:
            self.download_file(file['id'], file['name'])
    
    def authenticate(self): # Authenticate with Google Drive and return OAuth credentials
        if self.drive_service is None:
            if self.token_exists():
                credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            else:
                flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS, SCOPES)
                credentials = flow.run_local_server(port=0)
                with open('token.json', "w") as token:
                    token.write(credentials.to_json())
            self.drive_service = build(SERVICE, API_VERSION, credentials=credentials)
        return self.drive_service
    
    def token_exists(self):
        return Path(TOKEN_FILE).exists() 
    
    def download_file(self, file_id, file_name):
        request = self.drive_service.files().get_media(fileId = file_id)
        destination = self.destination_path / file_name
        with open(destination, "wb") as file:
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()

    def find_missing_files(self):
        results = self.drive_service.files().list(
            q=f"'{FOLDER_ID}' in parents and trashed = false",
            fields="nextPageToken, files(id, name, mimeType)"
        ).execute()
        files = results.get('files', [])
        destination_file_name_set = {file.name for file in self.destination_path.iterdir() if file.is_file()}
        missing_files = [file for file in files if file['name'] not in destination_file_name_set]
        return missing_files