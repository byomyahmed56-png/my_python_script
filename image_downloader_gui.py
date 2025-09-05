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

# وظيفة اختيار المجلد
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)

# إنشاء النافذة
root = tk.Tk()
root.title("Image Downloader")
root.geometry("600x200")

# الصف الأول: رابط الصورة
tk.Label(root, text="Image URL:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

# الصف الثاني: المجلد
tk.Label(root, text="Save Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
folder_entry = tk.Entry(root, width=40)
folder_entry.grid(row=1, column=1, padx=10, pady=10)
browse_btn = tk.Button(root, text="Browse", command=browse_folder)
browse_btn.grid(row=1, column=2, padx=10, pady=10)

# الصف الثالث: زر التحميل (في النص)
download_btn = tk.Button(root, text="Download", command=download_image, width=20)
download_btn.grid(row=2, column=0, columnspan=3, pady=20)

root.mainloop()
