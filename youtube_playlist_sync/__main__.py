#!/usr/bin/python3
import sys
import logging

from . import config
from .sync import Playlist


def main():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


    exit_code = 0

    if not config.get().sections():
        logging.info('No playlist to sync, take a look at your configuration file.')
        exit(exit_code)

    for conf in config.get().sections():
        try:
            Playlist(conf, config.get()[conf]['format'], config.get()[conf]['destination']).sync()
        except RuntimeError as e:
            logging.critical(str(e) + '\n')
            exit_code = 1

    exit(exit_code)


if __name__ == "__main__":
    main()
