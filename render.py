# render.py - Runs on Railway as a cron job
# Automatically generates satellite images and pushes to GitHub

import os
import base64
import requests
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ===== CONFIGURATION =====
GITHUB_USERNAME = "your-username"
REPO_NAME = "satellite-imagery"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # Set in Railway variables
BRANCH = "main"

# ===== GITHUB UPLOAD FUNCTION =====
def upload_to_github(local_file, remote_path, commit_message="Auto-update satellite image"):
    """Upload a file to GitHub repository"""
    
    with open(local_file, 'rb') as f:
        content = f.read()
    
    encoded = base64.b64encode(content).decode()
    
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{remote_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Check if file exists
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        sha = response.json()['sha']
        data = {
            "message": commit_message,
            "content": encoded,
            "sha": sha,
            "branch": BRANCH
        }
    else:
        data = {
            "message": commit_message,
            "content": encoded,
            "branch": BRANCH
        }
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print(f"✅ Uploaded: {remote_path}")
        return True
    else:
        print(f"❌ Failed: {response.status_code} - {response.json()}")
        return False

# ===== SATELLITE IMAGE GENERATION =====
def generate_satellite_images():
    """Generate satellite images - REPLACE with your actual code"""
    
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    print(f"\n{'='*50}")
    print(f"🛰️ Satellite Render Job: {timestamp} UTC")
    print(f"{'='*50}")
    
    # ----- PLACEHOLDER: Replace with your actual satellite code -----
    # This is where you'd put your fetch_one_frame() and plot_frame() calls
    
    # Generate IR image
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='#0a0a1a')
    ax.set_facecolor('#0a0a1a')
    data = np.random.rand(200, 200) * 100
    im = ax.imshow(data, cmap='inferno')
    plt.colorbar(im, label='Brightness Temperature (°C)')
    ax.set_title(f'🛰️ Satellite IR - {timestamp}', color='white')
    ax.tick_params(colors='white')
    fig.savefig('/tmp/ir_latest.png', bbox_inches='tight', facecolor='#0a0a1a', dpi=80)
    plt.close(fig)
    print("✅ Generated IR image")
    
    # Generate Water Vapor image
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='#0a0a1a')
    ax.set_facecolor('#0a0a1a')
    data = np.random.rand(200, 200) * 80 - 40
    im = ax.imshow(data, cmap='coolwarm')
    plt.colorbar(im, label='Brightness Temperature (°C)')
    ax.set_title(f'💧 Water Vapor - {timestamp}', color='white')
    ax.tick_params(colors='white')
    fig.savefig('/tmp/wv_latest.png', bbox_inches='tight', facecolor='#0a0a1a', dpi=80)
    plt.close(fig)
    print("✅ Generated WV image")
    # ----------------------------------------------------------------
    
    return True

# ===== MAIN FUNCTION =====
def main():
    """Main job: generate images and push to GitHub"""
    
    print("🚀 Starting satellite render job...")
    
    # Generate images
    if not generate_satellite_images():
        print("❌ Failed to generate images")
        return
    
    # Upload to GitHub
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    uploads = [
        ("/tmp/ir_latest.png", "images/ir_latest.png", f"Update IR image - {timestamp}"),
        ("/tmp/wv_latest.png", "images/wv_latest.png", f"Update WV image - {timestamp}"),
    ]
    
    for local_path, remote_path, message in uploads:
        if os.path.exists(local_path):
            upload_to_github(local_path, remote_path, message)
    
    print(f"\n✅ Job complete at {timestamp}")
    print("🌐 View at: https://{}.github.io/{}/".format(GITHUB_USERNAME, REPO_NAME))

if __name__ == "__main__":
    main()
