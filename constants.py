"""
Auther Vishnu.

Will have all necessary constants.
"""
import os

from git import Repo

repo = Repo(".")
repo_root = repo.git.rev_parse("--show-toplevel")
# Configs
config_dir = "configs"
config_dir_path = os.path.join(repo_root, config_dir)
config_file = "config.json"
config_file_path = os.path.join(config_dir_path, config_file)
# default Playlist dir
default_playlist_dir = "playlist_directory"
default_playlist_path = os.path.join(repo_root, default_playlist_dir)
