# arXive common

from json import load
from subprocess import run
from os import path, remove, rmdir

def load_config():
    with open('config.json', 'r') as file:
        return load(file)

def get_deletions(source, destination):
    cmd = ["rsync", "-av", "--delete", "--dry-run", source, destination]
    result = run(cmd, capture_output=True, text=True)
    deletions = []
    for line in result.stdout.splitlines():
        if line.startswith("deleting "):
            filepath = line[len("deleting "):].strip()
            deletions.append(filepath)
    return deletions

# TODO a distinct function for CLI/GUI bc of printing?
def prompt_and_delete(files, destination):
    for file in files:
        full_path = path.join(destination, file)
        print(f"\nFile to delete: {full_path}")
        choice = input("Delete this file? [y/N]: ").strip().lower()
        if choice == "y":
            try:
                remove(full_path)  # FIXME fails if its a directory (rmdir)
                print(f"Deleted: {full_path}")
            except Exception as e:
                print(f"Error deleting {full_path}: {e}")
        else:
            print(f"Skipped: {full_path}")