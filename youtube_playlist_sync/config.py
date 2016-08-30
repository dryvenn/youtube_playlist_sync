#!/usr/bin/python3
import os
import re
import logging
import configparser


try:
    _CONFIG_PATH = os.path.abspath(os.getenv('XDG_CONFIG_HOME'))
except AttributeError:
    _CONFIG_PATH = os.path.abspath(os.path.expanduser('~/.config'))
finally:
    _CONFIG_PATH = os.path.join(_CONFIG_PATH, 'youtube_playlist_sync.ini')


_default_config = {
    'format': "mp4",
    'destination': "~/Music/youtube-playlist-sync",
}


def _parse():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(_CONFIG_PATH))

    # Add defaults when there is none
    for key, val in _default_config.items():
        if key not in config['DEFAULT']:
            config['DEFAULT'][key] = val

    # Replace urls by ids
    for s in config.sections():
        if 'list' in s:
            val = dict(config.items(s))
            config.remove_section(s)
            new_s = re.search('list=((?:\w|-)+)', s).group(1)
            config[new_s] = val
        else:
            assert re.fullmatch('\w+', s)

    # Log
    logstr = 'CONFIGURATION\n'
    for s in config.sections():
        logstr += '> id: ' + s + '\n'
        for k in config[s]:
            v = config[s][k]
            logstr += '> ' + k + ': ' + v + '\n'
        logstr += '> \n'
    logging.debug(logstr)

    return config


_config = None


def get():
    """
    Don't parse at import, wait for this call.
    This allow things to get set up (eg logging level).
    """
    global _config
    if not _config:
        _config = _parse()
    return _config
