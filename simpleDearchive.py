#Requires the following libraries to be installed:
# pip install py7zr rarfile

import tkinter as tk
from tkinter import filedialog
import os
import zipfile
import tarfile
import py7zr
import rarfile
rarfile.UNRAR_TOOL = r"C:\Program Files\UnRAR\UnRAR.exe"

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
            print(f' [DIR]  {item}')
        else:
            print(f' [FILE] {item}')

# Function to find archive files in the selected folder
def find_archive_files(folder_path):
    archive_extensions = ['.zip', '.tar', '.tar.gz', '.rar', '.7z', '.gz', '.bz2']
    archive_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in archive_extensions):
                size_mb = os.path.getsize(os.path.join(root, file)) / (1024 * 1024)
                archive_files.append((file, {'size_mb': round(size_mb, 2)}))

    return archive_files

# Function to peek inside archive files
def peek_inside_archive(file_path):
    print(f"Peeking inside archive: {os.path.basename(file_path)}")
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.zip':
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            file_list = zip_ref.infolist()
            for item in file_list:
                size_mb = round(item.file_size / (1024 * 1024), 2)
                print(f"  {item.filename} - {size_mb} MB")
    elif ext == '.7z':
        with py7zr.SevenZipFile(file_path, mode='r') as seven_zip_ref:
            file_list = seven_zip_ref.getnames()
            for item in file_list:
                print(f"  {item.filename} - {size_mb} MB")
    else:
        print(f"Peeking not supported for {ext} files.")
    return file_list



def unzip_any(archive_path, output_folder=None):
    ext = os.path.splitext(archive_path)[1].lower()
    name = os.path.splittext(os.path.basename(archive_path))[0]
    output_folder = output_folder or os.path.join(os.path.dirname(archive_path), name)

    if ext == '.zip':
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(path=output_folder)
    elif ext == '.7z':
        with py7zr.SevenZipFile(archive_path, mode='r') as seven_zip_ref:
            seven_zip_ref.extractall(path=output_folder)
    elif ext == '.rar':
        with rarfile.RarFile(archive_path) as rar_ref:
            rar_ref.extractall(path=output_folder)
    elif ext in ['.tar', '.gz', 'bz2', '.tar.gz', '.tgz']:
        with tarfile.open(archive_path, 'r:*') as tar_ref:
            tar_ref.extractall(output_folder)
    else:
        print(f"Unsupported archive format: {ext}")
        return None
    print(f"Extracted '{archive_path}' to '{output_folder}'")
    return output_folder

# Run program  
folder = select_folder()
if folder:
    list_contents(folder)
    archive_files = find_archive_files(folder)
    print(f"\nFound {len(archive_files)} archive files:")
    for file in archive_files:
        print(f"  {file}")
        if archive_files:
            peek_inside_archive(os.path.join(folder, archive_files[0][0]))