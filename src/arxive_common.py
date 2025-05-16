# arXive common

from json import load, dump
from subprocess import run
from os import path, remove, rmdir


def load_config():
    config_path = path.expanduser('~/.config/arxive.json')
    try:
        if path.exists(config_path):
            with open(config_path, 'r') as file:
                return load(file)
        else:
            with open(config_path, 'w') as file:
                config = {'source': "", 'destination': ""}
                dump(config, file)
                return config
    except Exception as e:
        # TODO write errors to log file
        print(f"Error: {e}")

def save_config(config):
    try:
        with open(path.expanduser('~/.config/arxive.json'), 'w') as file:
            dump(config, file)
    except Exception as e:
        # TODO write errors to log file
        print(f"Error: {e}")


def get_deletions(source, destination):
    cmd = ["rsync", "-av", "--delete", "--dry-run", source, destination]
    deletions = []
    try:
        result = run(cmd, capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if line.startswith("deleting "):
                filepath = line[len("deleting "):].strip()
                deletions.append(filepath)
    except Exception as e:
        # TODO write errors to log file
        print(f"Error: {e}")
    finally:
        return deletions


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
            # TODO write errors to log file
            print(f"Error deleting {file}: {e}")
