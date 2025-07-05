# arXive common

from json import load, dump
from subprocess import run
from os import path, remove, rmdir
from datetime import datetime


class DirWarning(Exception):
    def __init__(self, message):
        super().__init__(message)


class Config:
    config_path = path.expanduser('~/.config/arxive')

    def __init__(self):
        cfg_file = self.load()
        self.source = cfg_file['source']
        self.destination = cfg_file['destination']
        self.options = cfg_file['options']

    def load(self):
        if path.exists(self.config_path):
            with open(self.config_path, 'r', encoding="utf-8") as file:
                return load(file)
        else:
            raise Exception("Configuration file cannot be found at "
                            "~/.config/arxive.")

    def save(self):
        with open(self.config_path, 'w',
                  encoding="utf-8") as file:
            config = {"source": self.source, "destination": self.destination,
                      "options": self.options}
            dump(config, file)


class Session:
    log_path = (f"{path.dirname(path.dirname(path.abspath(__file__)))}"
                f"/session.log")

    def __init__(self):
        self.init_log()
        self.source = None
        self.destination = None
        self.options = None
        self.deletions = None
        self.deleted, self.errors = 0, 0

    def init_log(self):
        with open(self.log_path, 'w', encoding="utf-8") as log:
            log.write(f"=============================================\n"
                      f"arXive session log -- "
                      f"{datetime.now().strftime("%Y %b %d. - %X")}\n"
                      f"=============================================\n")

    def log(self, msg, exception=None):
        print(msg)
        if exception:
            msg = f"{msg} - {exception}"
        with open(self.log_path, 'a', encoding="utf-8") as log:
            log.write(f"{msg}\n")

    def get_deletions(self):
        if self.source == self.destination:
            raise DirWarning("Warning: source and destination "
                             "can not be the same directory!")
        cmd = ["rsync", "-av", "--delete", "--dry-run",
               self.source, self.destination]
        deletions = []
        result = run(cmd, capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if line.startswith("deleting "):
                filepath = line[len("deleting "):].strip()
                deletions.append(filepath)
        return deletions

    def delete_entity(self, entity_path):
        if path.isfile(entity_path):
            remove(entity_path)
            self.deleted += 1
        elif path.isdir(entity_path):
            rmdir(entity_path)
            self.deleted += 1
        else:
            raise Exception(f"Error: {entity_path} could not be deleted.")

    def sync(self):
        cmd = ["rsync", "-av"]
        if self.options:
            for option in self.options:
                cmd.append(option)
        cmd.extend([self.source, self.destination])
        return run(cmd, text=True, capture_output=True)


def create_session_log():
    base_path = path.dirname(path.dirname(path.abspath(__file__)))
    with open(f'{base_path}/session.log', 'w', encoding="utf-8") as log:
        log.write(f"=============================================\n"
                  f"arXive session log -- "
                  f"{datetime.now().strftime("%Y %b %d. - %X")}\n"
                  f"=============================================\n")

def write_log(msg, exception=None):
    print(msg)
    if exception:
        msg = f"{msg} - {exception}"
    with open('session.log', 'a', encoding="utf-8") as log:
        log.write(f"{msg}\n")

def load_config():
    config_path = path.expanduser('~/.config/arxive')
    if path.exists(config_path):
        with open(config_path, 'r', encoding="utf-8") as file:
            return load(file)
    else:
        raise Exception("Configuration file cannot be found at "
                        "~/.config/arxive.")

def save_config(config):
    with open(path.expanduser('~/.config/arxive'), 'w',
              encoding="utf-8") as file:
        dump(config, file)

def get_deletions(source, destination):
    if source == destination:
        raise DirWarning("Warning: source and destination "
                         "can not be the same directory!")
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

def sync(source, destination, options=None):
    cmd = ["rsync", "-av"]
    if options:
        for option in options:
            cmd.append(option)
    cmd.extend([source, destination])
    return run(cmd, text=True, capture_output=True)
