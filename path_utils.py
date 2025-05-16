from os.path import join, dirname, exists
import os

def join_dirname(*paths:str) -> str:
    return join(dirname(__file__), *paths)

def check_file_exists(file_path:str):
    return exists(file_path)

def remove_path(file_path:str) -> str:
    return os.path.basename(file_path)