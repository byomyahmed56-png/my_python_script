import requests
import os

url = "https://upload.wikimedia.org/wikipedia/commons/e/e4/Wikimedia_Hackathon_2025_Group_photo_from_drone.jpg"
folder = "images"

os.makedirs(folder, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    filename = url.split("/")[-1]  # اسم الصورة من الرابط
    with open(os.path.join(folder, filename), "wb") as f:
        f.write(response.content)
    print("Image downloaded successfully!")
else:
    print(f"Failed to download image. Status code: {response.status_code}")
