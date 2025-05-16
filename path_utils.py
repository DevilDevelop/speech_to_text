from os.path import join, dirname, exists

def join_dirname(*paths:str) -> str:
    return join(dirname(__file__), *paths)

def check_file_exists(file_path:str):
    return exists(file_path)