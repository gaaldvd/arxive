# arXive common

from json import load, dump
from subprocess import run
from os import path, remove, rmdir
from datetime import datetime


def create_session_log():
    base_path = path.dirname(path.dirname(path.abspath(__file__)))
    with open(f'{base_path}/session.log', 'w', encoding="utf-8") as log:
        log.write(f"=============================================\n"
                  f"arXive session log -- "
                  f"{datetime.now().strftime("%Y %b %d. - %X")}\n"
                  f"=============================================\n")


def load_config():
    config_path = path.expanduser('~/.config/arxive.json')
    if path.exists(config_path):
        with open(config_path, 'r', encoding="utf-8") as file:
            return load(file)
    else:
        with open(config_path, 'w', encoding="utf-8") as file:
            config = {}
            dump(config, file)
            return config


def save_config(config):
    with open(path.expanduser('~/.config/arxive.json'), 'w',
              encoding="utf-8") as file:
        dump(config, file)


def get_deletions(source, destination):
    cmd = ["rsync", "-av", "--delete", "--dry-run", source, destination]
    deletions = []
    result = run(cmd, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith("deleting "):
            filepath = line[len("deleting "):].strip()
            deletions.append(filepath)
    return deletions


def delete_entity(entity_path):
    if path.isfile(entity_path):
        remove(entity_path)
    elif path.isdir(entity_path):
        rmdir(entity_path)
    else:
        raise Exception(f"Error: {entity_path} could not be deleted")


def sync(source, destination):
    cmd = ["rsync", "-av", source, destination]
    return run(cmd, text=True, capture_output=True)
