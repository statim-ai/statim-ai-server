import importlib
import os

def get_directories_from_path(path):
    directories = []
    
    for _, subdirs, _ in os.walk(path):
        for dir in subdirs:
            directories.append(dir)

    return directories
