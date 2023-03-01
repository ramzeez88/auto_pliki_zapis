"""
This script automates the process of moving files between four folders ('archive', 'day before yesterday', 'yesterday', 'today')
in the 'Documents' folder. It moves files with a change in date at midnight. When files are moved from 'today' to 'yesterday', 
from 'yesterday' to 'day before yesterday', and from 'day before yesterday' to 'archive'. Files in the 'archive' folder are not moved.
"""

import os
import shutil
import datetime
import time

def create_folders():
    """
    Creates the four folders ('archive', 'day before yesterday', 'yesterday', 'today') in the 'Documents' folder, if they don't exist.
    """
    path_to_folder = os.path.join(os.path.expanduser("~"), "Documents")
    for folder in ['archive', 'day before yesterday', 'yesterday', 'today']:
        folder_path = os.path.join(path_to_folder, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

def move_files(source, destination):
    """
    Moves all files from the source folder to the destination folder.
    """
    for file in os.listdir(source):
        file_path = os.path.join(source, file)
        if os.path.isfile(file_path):
            shutil.move(file_path, destination)

def check_for_date_change():
    """
    Checks if the current date has changed since the last known date, and moves files to the appropriate folders if necessary.
    """
    # Load the last known date from a file
    path_to_folder = os.path.join(os.path.expanduser("~"), "Documents")
    last_date_file = os.path.join(path_to_folder, "last_date.txt")
    if os.path.isfile(last_date_file):
        with open(last_date_file, "r") as f:
            last_date_str = f.read()
            last_date = datetime.datetime.strptime(last_date_str, "%Y-%m-%d")
    else:
        # If the file does not exist, set the last known date to the current date
        last_date = datetime.datetime.now().date()

    # Check if the current date is different from the last known date
    current_date = datetime.datetime.now().date()
    if current_date > last_date:
        # Move files from 'today' to 'yesterday'
        move_files(os.path.join(path_to_folder, 'today'), os.path.join(path_to_folder, 'yesterday'))

        # Move files from 'yesterday' to 'day before yesterday'
        move_files(os.path.join(path_to_folder, 'yesterday'), os.path.join(path_to_folder, 'day before yesterday'))

        # Move files from 'day before yesterday' to 'archive'
        move_files(os.path.join(path_to_folder, 'day before yesterday'), os.path.join(path_to_folder, 'archive'))

        # Save the current date to the file
        with open(last_date_file, "w") as f:
            f.write(str(current_date))


if __name__ == '__main__':
    create_folders()
    check_for_date_change()
    while True:
        now = datetime.datetime.now()
        
        # Check if it's midnight
        if now.hour == 0 and now.minute == 0:
            # Move files from 'today' to 'yesterday'
            move_files(os.path.join(path_to_folder, 'today'), os.path.join(path_to_folder, 'yesterday'))
            
            # Move files from 'yesterday' to 'day before yesterday'
            move_files(os.path.join(path_to_folder, 'yesterday'), os.path.join(path_to_folder, 'day before yesterday'))
            
            # Move files from 'day before yesterday' to 'archive'
            move_files(os.path.join(path_to_folder, 'day before yesterday'), os.path.join(path_to_folder, 'archive'))
        
        time.sleep(300) # Wait 5 minutes before checking again
