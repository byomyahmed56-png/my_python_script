import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import os

# وظيفة تنزيل الصورة
def download_image():
    url = url_entry.get()
    folder = folder_entry.get() or "images"
    
    if not url.strip():
        messagebox.showwarning("Warning", "Please enter an image URL!")
        return
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        filename = os.path.join(folder, url.split("/")[-1])
        with open(filename, "wb") as f:
            f.write(response.content)
        messagebox.showinfo("Success", f"Downloaded: {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download image:\n{e}")

# وظيفة اختيار المجلد عبر نافذة
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)

# إنشاء النافذة
root = tk.Tk()
root.title("Image Downloader")
root.geometry("500x200")

# واجهة المستخدم
tk.Label(root, text="Image URL:").pack(pady=(10,0))
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=(0,10))

tk.Label(root, text="Save Folder:").pack()
folder_entry = tk.Entry(root, width=50)
folder_entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))

browse_btn = tk.Button(root, text="Browse", command=browse_folder)
browse_btn.pack(side=tk.LEFT, padx=5, pady=(0,10))

download_btn = tk.Button(root, text="Download", command=download_image)
download_btn.pack(pady=(10,0))

root.mainloop()
