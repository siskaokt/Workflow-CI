from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import os

# Autentikasi pakai Service Account
gauth = GoogleAuth()
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scopes=["https://www.googleapis.com/auth/drive"]
)

drive = GoogleDrive(gauth)

# ID folder Google Drive tujuan
folder_id = "1FlgG-4LhGqah0vRlV8BcTJDiyWYxhzAr"

# File yang ingin di-upload
file_list = ["metric_info.json", "confusion_matrix.png", "estimator.html"]

for file_name in file_list:
    if os.path.exists(file_name):
        file = drive.CreateFile({
            'title': file_name,
            'parents': [{'id': folder_id}]
        })
        file.SetContentFile(file_name)
        file.Upload()
        print(f"{file_name} uploaded to Google Drive.")
    else:
        print(f"{file_name} NOT FOUND. Skipped.")
