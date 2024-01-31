from pytube import YouTube, Playlist
from pathlib import Path
import os
import threading
import re


def on_progress_callback(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"\rDownloading: {percentage:.2f}% complete", end='', flush=True)


def download_with_progress(stream, output_path, callback):
    stream.download(output_path=output_path)
    callback(stream, None, 0)  # Print 100% when download is complete


def download_playlist(playlist_url, output_path='.'):
    # Create Playlist object
    playlist = Playlist(playlist_url)
    playlist_title = playlist.title
    playlist_dir = playlist_title.replace(" ", "_")
    playlist_path = os.path.join(output_path, playlist_dir)
    Path(playlist_path).mkdir(parents=True, exist_ok=True)
    # Display playlist information
    print(f"Playlist Title: {playlist.title}")
    print(f"Number of Videos in Playlist: {len(playlist.video_urls)}")
    # Download each video in the playlist
    for video_url in playlist.video_urls:
        video = YouTube(video_url)
        import pdb;pdb.set_trace()
        video_title = video.title
        video_file = re.sub(r'[^a-zA-Z0-9]+', '_', video_title.replace(' ', '_'))
        video_file_path = os.path.join(playlist_path, f'{video_file}.mp4')
        if not os.path.exists(video_file_path) or os.path.getsize(video_file_path) == 0:
            print(f"Downloading: {video.title}")
            only_audio = video.streams.filter(only_audio=True)
            if only_audio:
                print(f"Only Audio {video_title}")
            else:
                print(f"Video and Audio {video_title}")
            video_streams = video.streams.get_highest_resolution()
            video_stream = video_streams
            video_stream.download(output_path=playlist_path, filename=video_file)
            # video.streams.get_highest_resolution().download(output_path=playlist_path, on_progress_callback=on_progress_callback)
    print(f"\nPlaylist downloaded successfully to: {playlist_path}")


if __name__ == "__main__":
    # Replace 'YOUR_PLAYLIST_URL' with the actual URL of the YouTube playlist
    playlist_url = 'https://www.youtube.com/playlist?list=PLKpX5mL0zzkjv1wnEmUmENE1rcFnsSIU_'

    # Replace 'YOUR_OUTPUT_PATH' with the desired output directory
    output_directory = os.path.join('youtube_playlists')

    download_playlist(playlist_url, output_directory)
