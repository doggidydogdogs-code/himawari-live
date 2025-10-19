from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Authenticate Google Drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # First time only; follow instructions
drive = GoogleDrive(gauth)

# Create a dummy file to upload
with open("data/test_file.txt", "w") as f:
    f.write("Hello SATAID! This is a test.")

# Upload to Google Drive
file = drive.CreateFile({'title': 'test_file.txt',
                         'parents':[{'id': '1Rh_ACRtQC2itd8lqfoJd4a3FQOmFD9Mn'}]})
file.SetContentFile("data/test_file.txt")
file.Upload()

print("✅ Test file uploaded successfully!")
