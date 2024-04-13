"""Module with usefull functions."""

import os


def get_directories_from_path(path):
    """Get all directories and subdirectories from a given path."""
    directories = []

    for _, subdirs, _ in os.walk(path):
        for directory in subdirs:
            directories.append(directory)

    return directories
