# YouTube Playlist Sync

This small script aims to synchronize YouTube playlists on a local machine.

It is intended to be run periodically (eg with cron).


## Usage

```bash
> youtube_playlist_sync
```


## Configuration

> As the script doesn't support any authentication, make sure all playlists are either 'Public' or 'Unlisted'.

The script will look for a configuration file named `youtube_playlist_sync.ini` under `$XDG_CONFIG_HOME` or if this variable is not defined under `~/.config`.

### youtube_playlist_sync.ini file example

```ini
# Default parameters
[DEFAULT]
# Output format (will default to 'mp4' if not specified).
# See `youtube_dl' for more info.
format: mp3
# Output directory (will default to '~/Music/youtube-playlist-sync' if not specified).
# The playlist will live in a subdirectory of this one.
destination: ~/Music

# A playlist
[https://www.youtube.com/playlist?list=PLjqNIb_ZU6K8Jh_Q01s4qXPV6n9Y1a-JW]
format: mp4
```
