"""
Author Vishnu.

Download youtube playlist with playlist id
"""
import json
import os
from pathlib import Path
import re

from pytube import YouTube, Playlist
from retry import retry

import constants


def load_json_file(config_file: str = constants.config_file_path) -> dict:
    """
    Load json Config file
    Args:
        config_file (str): Path to the json file

    Returns:
        Config Dict loaded from json

    """
    with open(config_file, "r") as json_config:
        config_dict = json.load(json_config)
        return config_dict


@retry(delay=2, tries=6)
def download_yt_video(
        video_url: str,
        playlist_path: str,
        codec_type: str = "audio",
        file_type: str = "mp4",
        playlist_data: list = None
):
    """

    Args:
        video_url:
        playlist_path:
        codec_type:
        file_type:
        playlist_data:

    Returns:

    """
    video = YouTube(video_url)
    video_title = video.title
    video_file = re.sub(r'[^a-zA-Z0-9]+', '_', video_title.replace(' ', '_'))
    dest_file_name = f'{video_file}.{file_type}'
    dest_file_path = os.path.join(playlist_path, dest_file_name)
    print(f"checking: {video.title}")
    if os.path.exists(dest_file_path) and playlist_data:
        actual_file_size = os.path.getsize(dest_file_path)
        filtered_song = [song for song in playlist_data if song["song_name"] == dest_file_name]
        if filtered_song:
            expected_file_size = filtered_song[0]["file_size"]
        else:
            expected_file_size = 0
        if actual_file_size == expected_file_size and expected_file_size != 0:
            return None
    streams = video.streams
    if codec_type == "audio":
        stream = streams.get_audio_only()
    else:
        stream = streams.get_highest_resolution()
    print(f"Downloading: {video.title}")
    stream.download(output_path=playlist_path, filename=dest_file_name)
    title_dict = {"song_name": dest_file_name, "expected_size": stream.filesize}
    return title_dict


def download_playlist(playlist_url, output_path=constants.default_playlist_path, codec_type="audio"):
    """
    Download the playlist
    Args:
        playlist_url: playlist url
        output_path: playlist dir to which the playlist needs to be saved

    Returns:

    """
    # Create Playlist object
    playlist = Playlist(playlist_url)
    playlist_title = playlist.title
    playlist_dir = playlist_title.replace(" ", "_")
    playlist_path = os.path.join(output_path, playlist_dir)
    dest_dir = os.path.join(playlist_path, codec_type)
    Path(dest_dir).mkdir(parents=True, exist_ok=True)
    # Display playlist information
    print(f"Playlist Title: {playlist.title}")
    print(f"Number of Videos in Playlist: {len(playlist.video_urls)}")
    # Download each video in the playlist
    url_list = playlist.video_urls
    playlist_data_file = "playlist.json"
    playlist_data_path = os.path.join(dest_dir, playlist_data_file)
    if os.path.exists(playlist_data_path):
        playlist_data = load_json_file(playlist_data_path)
    else:
        playlist_data = []
    for video_url in url_list:
        download_yt_video(video_url, dest_dir)
    # download_yt_video(url_list[0], playlist_path)
    print(f"\nPlaylist downloaded successfully to: {playlist_path}")


if __name__ == "__main__":
    # Replace 'YOUR_PLAYLIST_URL' with the actual URL of the YouTube playlist
    youtube_url = "https://www.music.youtube.com"
    playlist_endpoint = f"{youtube_url}/playlist?list="
    josn_config_dict = load_json_file()
    playlist_id = josn_config_dict["playlist_id"]
    url = f"{playlist_endpoint}{playlist_id}"
    # plist_url = 'https://www.youtube.com/playlist?list=PLKpX5mL0zzkjv1wnEmUmENE1rcFnsSIU_'
    # Replace 'YOUR_OUTPUT_PATH' with the desired output directory
    playlist_directory = josn_config_dict["playlist_directory"]
    if os.path.exists(playlist_directory):
        output_directory = josn_config_dict["playlist_directory"]
    else:
        output_directory = constants.default_playlist_path
    download_playlist(url, output_directory)
