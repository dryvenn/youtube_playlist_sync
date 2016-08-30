#!/usr/bin/python3
import sys
import logging

from sync import Playlist
import config


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


exit_code = 0

for conf in config.get().sections():
    try:
        Playlist(conf, config.get()[conf]['format'], config.get()[conf]['destination']).sync()
    except RuntimeError as e:
        logging.critical(str(e) + '\n')
        exit_code = 1

exit(exit_code)
