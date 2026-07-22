from pathlib import Path
import shutil
from google_auth_oauthlib.flow import InstalledAppFlow
from settings import *

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

class DriveSync:
    def __init__(self, source, destination):
        self.source_path = Path(source)
        self.destination_path = Path(destination)

    def sync(self): # Compare source folder files and destination folder files and copy any missing files
        source_file_name_set = {file.name for file in self.source_path.iterdir() if file.is_file()}
        destination_file_name_set = {file.name for file in self.destination_path.iterdir() if file.is_file()}
        missing_files = source_file_name_set - destination_file_name_set
        for file_name in missing_files:
            file_path = self.source_path / file_name
            shutil.copy(file_path, self.destination_path)
    
    def authenticate(self): # Authenticate with Google Drive and return OAuth credentials
        flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS, SCOPES)
        credentials = flow.run_local_server(port=0)
        return credentials