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
                full_path = os.path.join(root, file)
                size_mb = os.path.getsize(full_path) / (1024 * 1024)
                archive_files.append((full_path, {'size_mb': round(size_mb, 2)}))

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
            file_list = seven_zip_ref.list()
            for item in file_list:
                size_mb = round(item.uncompressed / (1024 * 1024), 2) if item.uncompressed else 0
                print(f"  {item.filename} - {size_mb} MB")
    else:
        print(f"Peeking not supported for {ext} files.")
        return []
    return file_list

def extract_archive_to_folder(file_path, destination_folder):
    ext = os.path.splitext(file_path)[1].lower()
    archive_name = os.path.splitext(os.path.basename(file_path))[0]

    # Create a subfolder named after the archive, inside the destination
    output_folder = os.path.join(destination_folder, archive_name)
    os.makedirs(output_folder, exist_ok=True)

    print(f"Extracting: {os.path.basename(file_path)} → {output_folder}")

    if ext == '.zip':
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_folder)

    elif ext == '.7z':
        with py7zr.SevenZipFile(file_path, mode='r') as seven_zip_ref:
            seven_zip_ref.extractall(path=output_folder)

    elif ext in ('.tar', '.gz', '.tgz', '.bz2'):
        with tarfile.open(file_path, 'r:*') as tar_ref:
            tar_ref.extractall(output_folder)

    elif ext == '.rar':
        import rarfile
        with rarfile.RarFile(file_path, 'r') as rar_ref:
            rar_ref.extractall(output_folder)

    else:
        print(f"  Extraction not supported for {ext} files.")
        return None

    return output_folder

# Run program  
folder = select_folder()
if folder:
    list_contents(folder)
    archive_files = find_archive_files(folder)
    print(f"\nFound {len(archive_files)} archive files:")

    # Create a destination folder for extracted files
    destination = os.path.join(folder, "extracted_archives")
    os.makedirs(destination, exist_ok=True)

    for full_path, info in archive_files:
        print(f"/nFound {len(archive_files)} archive files:")
        try:
            peek_inside_archive(full_path)
        except Exception as e:
            print(f" Error peeking into {full_path}: {e}")
        print(f" {os.path.basename(full_path)} - {info['size_mb']} MB")
        try:
            extract_archive_to_folder(full_path, destination)
        except Exception as e:
            print(f" Error extracting {full_path}: {e}")
            
