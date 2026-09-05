# from pathlib import Path
# import shutil
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from google.oauth2.credentials import Credentials
# from googleapiclient.http import MediaIoBaseDownload
# from settings import *
# import time

# SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# class DriveSync:
#     def __init__(self, destination):
#         self.destination_path = Path(destination)
#         self.drive_service = None

#     def sync_to_drive(self): # Compare drive folder files and destination folder files and download any missing files
#         self.authenticate()
#         print("Authentication Successful")        
#         missing_files = self.find_missing_files()
#         for index, file in enumerate(missing_files):
#             self.download_file(file['id'], file['name'])
#             print(f"Updating {index}/{len(missing_files)} files/")
    
#     def authenticate(self): # Authenticate with Google Drive and return OAuth credentials
#         print("Authenticating...")
#         if self.drive_service is None:
#             if self.token_exists():
#                 credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS, SCOPES)
#                 credentials = flow.run_local_server(port=0)
#                 with open('token.json', "w") as token:
#                     token.write(credentials.to_json())
#             self.drive_service = build(SERVICE, API_VERSION, credentials=credentials)
#         return self.drive_service
    
#     def token_exists(self): # Verify that authentication already exists so credentials don't need to be generated every time. 
#         return Path(TOKEN_FILE).exists() 
    
#     def download_file(self, file_id, file_name): # Download file from drive to local hard drive
#         request = self.drive_service.files().get_media(fileId = file_id)
#         destination = self.destination_path / file_name
#         with open(destination, "wb") as file:
#             downloader = MediaIoBaseDownload(file, request)
#             done = False
#             while not done:
#                 status, done = downloader.next_chunk()

#     def find_missing_files(self): # List the files that are in google drive but not on hard drive
#         print("Comparing local photos to drive")
#         start = time.perf_counter()
#         results = self.drive_service.files().list(
#             q=f"'{FOLDER_ID}' in parents and trashed = false",
#             fields="nextPageToken, files(id, name, mimeType)"
#         ).execute()

#         print(f"Google query: {time.perf_counter()-start:.3f}s")
#         start = time.perf_counter()

#         files = results.get('files', [])

#         print(f"Extract files: {time.perf_counter()-start:.6f}s")
#         start = time.perf_counter()

#         destination_file_name_set = {file.name for file in self.destination_path.iterdir() if file.is_file()}
#         missing_files = [file for file in files if file['name'] not in destination_file_name_set]
        
#         print(f"Comparison: {time.perf_counter()-start:.6f}s")

#         return missing_files


from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
from settings import *
import time


SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


class DriveSync:
    def __init__(self, destination):
        self.destination_path = Path(destination)
        self.drive_service = None

    def sync_to_drive(self):
        """Make the local image folder match the Google Drive folder."""

        self.authenticate()
        print("Authentication Successful")

        drive_files = self.get_drive_files()

        drive_file_names = {
            file['name']
            for file in drive_files
            if Path(file['name']).suffix.lower() in SUPPORTED_IMAGE_FILES
        }

        local_files = {
            file.name
            for file in self.destination_path.iterdir()
            if file.is_file()
            and file.suffix.lower() in SUPPORTED_IMAGE_FILES
        }

        # Download files that are on Drive but not locally
        missing_files = [
            file
            for file in drive_files
            if file['name'] not in local_files
            and Path(file['name']).suffix.lower() in SUPPORTED_IMAGE_FILES
        ]

        for index, file in enumerate(missing_files):
            self.download_file(file['id'], file['name'])
            print(f"Downloaded {index + 1}/{len(missing_files)}: {file['name']}")

        # Delete files that are local but no longer on Drive
        deleted_files = [
            file_name
            for file_name in local_files
            if file_name not in drive_file_names
        ]

        for file_name in deleted_files:
            file_path = self.destination_path / file_name
            file_path.unlink()
            print(f"Deleted: {file_name}")

    def authenticate(self):
        """Authenticate with Google Drive."""

        print("Authenticating...")

        if self.drive_service is None:
            if self.token_exists():
                credentials = Credentials.from_authorized_user_file(
                    TOKEN_FILE,
                    SCOPES
                )
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    GOOGLE_CREDENTIALS,
                    SCOPES
                )

                credentials = flow.run_local_server(port=0)

                with open(TOKEN_FILE, "w") as token:
                    token.write(credentials.to_json())

            self.drive_service = build(
                SERVICE,
                API_VERSION,
                credentials=credentials
            )

        return self.drive_service

    def token_exists(self):
        """Check whether Google authentication already exists."""

        return Path(TOKEN_FILE).exists()

    def download_file(self, file_id, file_name):
        """Download a file from Google Drive to the local image folder."""

        request = self.drive_service.files().get_media(
            fileId=file_id
        )

        destination = self.destination_path / file_name

        with open(destination, "wb") as file:
            downloader = MediaIoBaseDownload(file, request)

            done = False

            while not done:
                status, done = downloader.next_chunk()

    def get_drive_files(self):
        """Return the files currently present in the Google Drive folder."""

        print("Comparing local photos to drive")

        start = time.perf_counter()

        results = self.drive_service.files().list(
            q=f"'{FOLDER_ID}' in parents and trashed = false",
            fields="nextPageToken, files(id, name, mimeType)"
        ).execute()

        print(f"Google query: {time.perf_counter() - start:.3f}s")

        return results.get('files', [])