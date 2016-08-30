#!/usr/bin/python3
import os
import re
import logging
import logging.handlers
from youtube_dl import YoutubeDL


def is_audio_format(fmt):
    """
    To know whether the file needs conversion.
    """
    return fmt in ['aac', 'mp3', 'm4a', 'wav']


class Downloader:
    """
    Do the actual downloading.
    """

    def __init__(self, fmt, dst_dir):
        logger = logging.getLogger('youtube_dl')
        logger.setLevel(logging.ERROR) # log ERROR, CRITICAL not DEBUG, INFO, WARNING
        logger.addHandler(logging.handlers.RotatingFileHandler('youtube_dl.log'))
        postprocessors = []
        if is_audio_format(fmt):
            postprocessors.append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': fmt,
            })
        ydl_opts = {
            'logger': logger,
            'postprocessors': postprocessors,
            'outtmpl': os.path.join(dst_dir, '%(title)s.%(id)s.%(ext)s'),
            'ignoreerrors': True,
            'quiet': True,
        }
        self.ydl = YoutubeDL(ydl_opts)

    def download(self, url):
        logging.info("Downloading %s", url)
        return self.ydl.download([url])


class Playlist:
    """
    Holds playlist info as defined in the config file.
    """

    def __init__(self, ytid, format, base_dir):
        """
        Note that `base_dir` is where the playlist's own directory will live.
        """
        self.ytid = ytid
        self.format = format
        base_dir = os.path.abspath(os.path.expandvars(os.path.expanduser(base_dir)))
        self.path = os.path.join(base_dir, self.get_info()['title'])
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        else:
            assert os.path.isdir(self.path)

    def get_info(self):
        """
        Download and cache playlist info.
        """
        try:
            return self._info
        except AttributeError:
            url = "https://www.youtube.com/playlist?list=" + self.ytid
            logging.info("Inspecting %s", url)
            ydl_opts = {'ignoreerrors': True, 'quiet': True}
            with YoutubeDL(ydl_opts) as ydl:
                ydl.add_default_info_extractors()
                self._info = ydl.extract_info(url, download=False)
                if not self._info:
                    raise RuntimeError('Bad playlist url ' + url)
            return self._info

    def scan(self):
        """
        Scan the dir for items, return the ones already there.
        """
        ytids = []
        items = os.listdir(self.path)
        for item in items:
            match = re.search("\.((?:\w|-)+)\.(\w{3})$", item)
            if match: # ignore non-item files
                if match.groups()[1] == self.format: # ignore other extensions
                    ytids.append(match.groups()[0])
        return ytids

    def sync(self):
        """
        Download missing items.
        """
        ytids = self.scan()
        dl = Downloader(self.format, self.path)
        for item in self.get_info()['entries']:
            item_ytid = item['id']
            if item_ytid not in ytids:
                dl.download("https://www.youtube.com/watch?v=" + item_ytid)
                ytids.append(item_ytid)
