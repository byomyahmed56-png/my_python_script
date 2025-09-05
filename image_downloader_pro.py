import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# وظيفة تنزيل صورة واحدة
def download_single_image(url, folder):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url.strip(), headers=headers)
        response.raise_for_status()
        filename = os.path.join(folder, url.split("/")[-1])
        with open(filename, "wb") as f:
            f.write(response.content)
        return f"✅ {filename}"
    except Exception as e:
        return f"❌ Failed: {url} ({e})"

# اختيار مجلد الحفظ
def browse_folder(entry_widget):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, folder_selected)

# ----------- تبويب 1: صورة واحدة ----------- #
def download_from_single():
    url = single_url_entry.get()
    folder = single_folder_entry.get() or "images"

    if not url.strip():
        messagebox.showwarning("Warning", "Please enter an image URL!")
        return

    if not os.path.exists(folder):
        os.makedirs(folder)

    result = download_single_image(url, folder)
    messagebox.showinfo("Result", result)

# ----------- تبويب 2: روابط متعددة ----------- #
def download_from_list():
    urls = multi_text_box.get("1.0", tk.END).strip().split("\n")
    folder = multi_folder_entry.get() or "images"

    if not urls or urls == [""]:
        messagebox.showwarning("Warning", "Please enter at least one image URL!")
        return

    if not os.path.exists(folder):
        os.makedirs(folder)

    results = []
    for url in urls:
        if url.strip():
            results.append(download_single_image(url, folder))

    messagebox.showinfo("Download Results", "\n".join(results))

# ----------- تبويب 3: صفحة ويب ----------- #
def download_from_webpage():
    page_url = webpage_url_entry.get()
    folder = webpage_folder_entry.get() or "images"

    if not page_url.strip():
        messagebox.showwarning("Warning", "Please enter a webpage URL!")
        return

    if not os.path.exists(folder):
        os.makedirs(folder)

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(page_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        img_tags = soup.find_all("img")

        if not img_tags:
            messagebox.showinfo("Result", "No images found on this page.")
            return

        results = []
        for img in img_tags:
            img_url = img.get("src")
            if img_url:
                full_url = urljoin(page_url, img_url)
                results.append(download_single_image(full_url, folder))

        messagebox.showinfo("Download Results", "\n".join(results))

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch webpage:\n{e}")

# ----------- الواجهة الرئيسية ----------- #
root = tk.Tk()
root.title("Image Downloader Pro")
root.geometry("700x500")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# تبويب 1: صورة واحدة
tab1 = tk.Frame(notebook)
notebook.add(tab1, text="Single URL")

tk.Label(tab1, text="Image URL:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
single_url_entry = tk.Entry(tab1, width=60)
single_url_entry.grid(row=0, column=1, padx=5, pady=10, columnspan=2)

tk.Label(tab1, text="Save Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
single_folder_entry = tk.Entry(tab1, width=40)
single_folder_entry.grid(row=1, column=1, padx=5, pady=10)
tk.Button(tab1, text="Browse", command=lambda: browse_folder(single_folder_entry)).grid(row=1, column=2, padx=5, pady=10)

tk.Button(tab1, text="Download", command=download_from_single).grid(row=2, column=0, columnspan=3, pady=20)

# تبويب 2: روابط متعددة
tab2 = tk.Frame(notebook)
notebook.add(tab2, text="Multiple URLs")

tk.Label(tab2, text="Enter Image URLs (one per line):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
multi_text_box = tk.Text(tab2, height=10, width=70)
multi_text_box.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

tk.Label(tab2, text="Save Folder:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
multi_folder_entry = tk.Entry(tab2, width=40)
multi_folder_entry.grid(row=2, column=1, padx=5, pady=10)
tk.Button(tab2, text="Browse", command=lambda: browse_folder(multi_folder_entry)).grid(row=2, column=2, padx=5, pady=10)

tk.Button(tab2, text="Download All", command=download_from_list).grid(row=3, column=0, columnspan=3, pady=20)

# تبويب 3: صفحة ويب
tab3 = tk.Frame(notebook)
notebook.add(tab3, text="Webpage Images")

tk.Label(tab3, text="Enter Webpage URL:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
webpage_url_entry = tk.Entry(tab3, width=60)
webpage_url_entry.grid(row=0, column=1, padx=5, pady=10, columnspan=2)

tk.Label(tab3, text="Save Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
webpage_folder_entry = tk.Entry(tab3, width=40)
webpage_folder_entry.grid(row=1, column=1, padx=5, pady=10)
tk.Button(tab3, text="Browse", command=lambda: browse_folder(webpage_folder_entry)).grid(row=1, column=2, padx=5, pady=10)

tk.Button(tab3, text="Download Images", command=download_from_webpage).grid(row=2, column=0, columnspan=3, pady=20)

root.mainloop()
