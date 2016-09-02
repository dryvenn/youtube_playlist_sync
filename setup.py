from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='youtube_playlist_sync',
    version='0.1.2',
    description='Syncs YouTube playlists locally',
    long_description=long_description,
    url='https://github.com/dryvenn/youtube_playlist_sync',
    author='dryvenn',
    author_email='dryvenn@gmail.com',
    license='MIT',
    keywords='youtube playlist download dl sync',
    packages=['youtube_playlist_sync'],
    install_requires=[
        'youtube_dl',
    ],
    entry_points={
        'console_scripts': [
            'youtube_playlist_sync=youtube_playlist_sync.__main__:main',
        ],
    },
)
