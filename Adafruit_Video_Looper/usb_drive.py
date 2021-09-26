# Copyright 2015 Adafruit Industries.
# Author: Tony DiCola
# License: GNU GPLv2, see LICENSE.txt
import glob

from .usb_drive_mounter import USBDriveMounter
import cv2
import numpy as np
import dropbox
from datetime import datetime

class USBDriveReader:

    # update them with your own credentials.
    app_key = "1v6wdxyvw7ozusj"
    app_secret = "2g8vsg62827ci4z"
    access_token = "sl.A5JKJ3g_Q5g7fD4tfz5mBn27wcKGdsciCoiOo6zPAMl60OvSu-91pB9WoetOIO18Euj-h8mdxDUeaNyBTVw6lf7I57DeTLgzK__CvA9auELcNOBhoJusdzk6BdVytkX8VXk-FpdwFjw"

    dbx = dropbox.Dropbox(access_token)

    dropbox_path = "Displex/"
    dropbox_download_path = "/media/pi/8C54-2740"

    # the path to the SD card video.
    sdcard_video_path = "/media/pi/8C54-2740/"
    sdcard_video_name = "video.mp4"

    exit = 0

    def get_video_to_play(dropbox_videos, sdcard_video_path):
        now = datetime.now()
        current_hour = int(now.strftime("%H"))

            if (current_hour >= 20 and current_hour < 22):
                # between 8pm to 10pm
                return dropbox_download_path + dropbox_videos[0]  # video1
            if (current_hour >= 22 and current_hour < 24):
                # between 10pm and 12am
                return dropbox_download_path + dropbox_videos[1]  # video2
            if (current_hour >= 0 and current_hour < 3):
                # between 12am to 3am
                return dropbox_download_path + dropbox_videos[2]  # video3
            if (current_hour >= 3 and current_hour < 20):
                # between 3am and 8pm
                return dropbox_download_path + dropbox_videos[2]  # video3
        else:
            print("No video found on DropBox")
            return sdcard_video_path + sdcard_video_name

    def __init__(self, config):
        """Create an instance of a file reader that uses the USB drive mounter
        service to keep track of attached USB drives and automatically mount
        them for reading videos.
        """
        self._load_config(config)
        self._mounter = USBDriveMounter(root=self._mount_path,
                                        readonly=self._readonly)
        self._mounter.start_monitor()


    def _load_config(self, config):
        self._mount_path = config.get('usb_drive', 'mount_path')
        self._readonly = config.getboolean('usb_drive', 'readonly')

    def search_paths(self):
        """Return a list of paths to search for files. Will return a list of all
        mounted USB drives.
        """
        self._mounter.mount_all()
        return glob.glob(self._mount_path + '*')

    def is_changed(self):
        """Return true if the file search paths have changed, like when a new
        USB drive is inserted.
        """
        return self._mounter.poll_changes()

    def idle_message(self):
        """Return a message to display when idle and no files are found."""
        return 'Insert USB drive with compatible movies.'


def create_file_reader(config, screen):
    """Create new file reader based on mounting USB drives."""
    return USBDriveReader(config)
