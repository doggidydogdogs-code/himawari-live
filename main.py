import s3fs
import os
import time
from datetime import datetime
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import subprocess  # To run the JMA converter

# -----------------------------
# CONFIGURATION
# -----------------------------
SAVE_FOLDER = "data"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Google Drive folder ID where SATAID files will be uploaded
GOOGLE_DRIVE_FOLDER_ID = "YOUR_FOLDER_ID_HERE"

# Path to the JMA converter (adjust if needed)
CONVERTER_PATH = "./ahi2sataid"

# -----------------------------
# GOOGLE DRIVE AUTHENTICATION
# -----------------------------
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # First time only, follow instructions
drive = GoogleDrive(gauth)

# -----------------------------
# MAIN LOOP
# -----------------------------
fs = s3fs.S3FileSystem(anon=True)

while True:
    # 1️⃣ Get latest HSD file path
    now = datetime.utcnow()
    path = f"noaa-himawari8/AHI-L1b-FLDK/{now:%Y/%m/%d}/"

    try:
        files = fs.ls(path)
        if not files:
            print("No files found today yet")
            time.sleep(600)
            continue
    except FileNotFoundError:
        print("Folder not ready yet")
        time.sleep(600)
        continue

    newest_file = sorted(files)[-1]
    local_hsd = os.path.join(SAVE_FOLDER, newest_file.split("/")[-1])

    # 2️⃣ Download if not already exists
    if not os.path.exists(local_hsd):
        fs.get(newest_file, local_hsd)
        print("✅ Downloaded HSD:", local_hsd)
    else:
        print("⏩ Already downloaded:", local_hsd)

    # 3️⃣ Convert HSD → SATAID using JMA converter
    dat_file = local_hsd.replace(".hsd", ".DAT")
    inf_file = local_hsd.replace(".hsd", ".INF")

    if not os.path.exists(dat_file) or not os.path.exists(inf_file):
        # Example: converter command, adjust if converter uses different args
        subprocess.run([CONVERTER_PATH, local_hsd, SAVE_FOLDER])
        print("✅ Converted to SATAID:", dat_file, inf_file)
    else:
        print("⏩ SATAID files already exist")

    # 4️⃣ Upload to Google Drive
    for file_path in [dat_file, inf_file]:
        file_name = os.path.basename(file_path)
        gfile = drive.CreateFile({'title': file_name,
                                  'parents':[{'id': GOOGLE_DRIVE_FOLDER_ID}]})
        gfile.SetContentFile(file_path)
        gfile.Upload()
        print("✅ Uploaded to Google Drive:", file_name)

    # 5️⃣ Wait 10 minutes before next check
    time.sleep(600)
