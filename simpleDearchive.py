import tkinter as tk
from tkinter import filedialog
import os

# Function to select a folder using a dialog
def select_folder():
    root = tk.Tk()
    root.withdraw()

    folder_path = tk.filedialog.askdirectory(title="Select a folder")

    if not folder_path:
        print("No folder selected. Exiting.")
        return None

    return folder_path
    
# Function to list contents of the selected folder
def list_contents(folder_path):
    contents = os.listdir(folder_path)
    print(f"Contents of '{folder_path}':")
    print(f'Contains {len(contents)} items:\n')

    for item in contents:
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            print(f'[DIR]  {item}')
        else:
            print(f' [FILE] {item}')

# Function to find archive files in the selected folder
def find_archive_files(folder_path):
    archive_extensions = ['.zip', '.tar', '.tar.gz', '.rar', '.7z']
    archive_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in archive_extensions):
                size_mb = os.path.getsize(os.path.join(root, file)) / (1024 * 1024)
                archive_files.append((file, {'size_mb': round(size_mb, 2)}))

    return archive_files

# Run program  
folder = select_folder()
if folder:
    list_contents(folder)
    archive_files = find_archive_files(folder)
    print(f"\nFound {len(archive_files)} archive files:")
    for file in archive_files:
        print(f"  {file}")
