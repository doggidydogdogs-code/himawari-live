import requests, os, time

# Example: Download latest Himawari-8 image tile
BASE_URL = "https://noaa-himawari.s3.amazonaws.com"
SAVE_DIR = "data"

os.makedirs(SAVE_DIR, exist_ok=True)

def get_latest_image():
    # This just downloads one small example file
    url = f"{BASE_URL}/himawari-8/AHI/full_disk_1km/R21/latest.jpg"
    r = requests.get(url)
    if r.status_code == 200:
        filename = os.path.join(SAVE_DIR, "latest.jpg")
        with open(filename, "wb") as f:
            f.write(r.content)
        print("Downloaded:", filename)
    else:
        print("Error downloading:", r.status_code)

while True:
    get_latest_image()
    time.sleep(600)  # 10 minutes
