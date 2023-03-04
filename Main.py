"""
This script automates the process of moving files between four folders ('archive', 'day before yesterday', 'yesterday', 'today')
in the 'Documents' folder. It moves files with a change in date at midnight. When files are moved from 'today' to 'yesterday', 
from 'yesterday' to 'day before yesterday', and from 'day before yesterday' to 'archive'. Files in the 'archive' folder are not moved.
"""
import os
import shutil
import datetime
import time

# Folder paths
doc_folder = os.path.join(os.path.expanduser('~'), 'Documents')
today_folder = os.path.join(doc_folder, 'today')
yesterday_folder = os.path.join(doc_folder, 'yesterday')
day_before_yesterday_folder = os.path.join(doc_folder, 'day_before_yesterday')
archive_folder = os.path.join(doc_folder, 'archive')
last_date_file = os.path.join(doc_folder, 'last_date.txt')

# Create folders if they don't exist
for folder in (today_folder, yesterday_folder, day_before_yesterday_folder, archive_folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

# Read the last program execution date
def get_last_date():
    try:
        with open(last_date_file, 'r') as f:
            last_date_str = f.read().strip()
            last_date = datetime.datetime.strptime(last_date_str, '%Y-%m-%d %H:%M:%S')
            return last_date
    except:
        last_date = datetime.datetime.now()
        return last_date

# Main program loop
while True:
    # Current date and time
    now = datetime.datetime.now()
    last_date = get_last_date()
    # Time difference in days
    delta = (now - last_date).days
    
    # Move files
    if delta == 1:
        for src, dst in [(day_before_yesterday_folder, archive_folder), (yesterday_folder, day_before_yesterday_folder),(today_folder, yesterday_folder)]:
            for file in os.listdir(src):
                src_file = os.path.join(src, file)
                dst_file = os.path.join(dst, file)
                shutil.move(src_file, dst_file)
    elif delta == 2:
        for src, dst in [(day_before_yesterday_folder, archive_folder), (yesterday_folder, archive_folder),(today_folder, day_before_yesterday_folder)]:
            for file in os.listdir(src):
                src_file = os.path.join(src, file)
                dst_file = os.path.join(dst, file)
                shutil.move(src_file, dst_file)
    elif delta >= 3:
        for src in [today_folder, yesterday_folder, day_before_yesterday_folder]:
            for file in os.listdir(src):
                src_file = os.path.join(src, file)
                dst_file = os.path.join(archive_folder, file)
                shutil.move(src_file, dst_file)

    # Update the last program execution date
    last_date = now
    with open(last_date_file, 'w') as f:
        f.write(last_date.strftime('%Y-%m-%d %H:%M:%S'))

    # Wait for one minute
    time.sleep(60)

