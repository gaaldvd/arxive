# arXive common

from json import load, dump
from subprocess import run
from os import path, remove, rmdir
from datetime import datetime


def load_config():
    config_path = path.expanduser('~/.config/arxive.json')
    try:
        if path.exists(config_path):
            with open(config_path, 'r', encoding="utf-8") as file:
                return load(file)
        else:
            with open(config_path, 'w', encoding="utf-8") as file:
                config = {}
                dump(config, file)
                return config
    except Exception as e:
        with open('session.log', 'a', encoding="utf-8") as log:
            log.write(f"Error: {e}")
        return False


def save_config(config):
    try:
        with open(path.expanduser('~/.config/arxive.json'), 'w',
                  encoding="utf-8") as file:
            dump(config, file)
        return True
    except Exception as e:
        with open('session.log', 'a', encoding="utf-8") as log:
            log.write(f"Error: {e}")
        return False


def create_session_log():
    base_path = path.dirname(path.dirname(path.abspath(__file__)))
    with open(f'{base_path}/session.log', 'w', encoding="utf-8") as log:
        log.write(f"=============================================\n"
                  f"arXive session log -- "
                  f"{datetime.now().strftime("%Y %b %d. - %X")}\n"
                  f"=============================================\n")


def get_deletions(source, destination):
    cmd = ["rsync", "-av", "--delete", "--dry-run", source, destination]
    deletions = []
    try:
        result = run(cmd, capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if line.startswith("deleting "):
                filepath = line[len("deleting "):].strip()
                deletions.append(filepath)
        return deletions
    except Exception as e:
        with open('session.log', 'a', encoding="utf-8") as log:
            log.write(f"Error: {e}")
        return False


def delete_files(files):
    for file in files:
        try:
            if path.isfile(file):
                remove(file)
            elif path.isdir(file):
                rmdir(file)
            else:
                raise Exception
        except Exception as e:
            with open('session.log', 'a', encoding="utf-8") as log:
                log.write(f"Error: {e}")
            return False
    return True


def sync(source, destination):
    cmd = ["rsync", "-av", source, destination]
    try:
        return run(cmd, text=True, capture_output=True)
    except Exception as e:
        with open('session.log', 'a', encoding="utf-8") as log:
            log.write(f"Error: {e}")
        return False
