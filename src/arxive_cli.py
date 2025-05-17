# arXive CLI script

from sys import argv
from arxive_common import *


def get_paths(config):
    if len(argv) > 1:
        source, destination = argv[1], argv[2]
        return source, destination
    elif config['source'] and config['destination']:
        source, destination = config['source'], config['destination']
        return source, destination
    else:
        source, destination = input("source: "), input("destination: ")
        choice = input("save as default? [y/N]: ").strip().lower()
        if choice == "y":
            save_config({'source': source, 'destination': destination})
        return source, destination


def prompt_deletions(files, destination):
    files_to_delete = []
    for file in files:
        full_path = path.join(destination, file)
        print(full_path)
        choice = input("delete? [y/N]: ").strip().lower()
        if choice == "y":
            files_to_delete.append(full_path)
    return files_to_delete


def main():
    """Main function."""

    config = load_config()
    print(f"configs: {config}")

    source, destination = get_paths(config)
    # TODO check if these are valid paths
    print(f"source: {source}\ndestination: {destination}")

    deletions = get_deletions(source, destination)
    print(f"deletions: {deletions}")

    files_to_delete = prompt_deletions(deletions, destination)
    print(f"files to delete: {files_to_delete}")

    delete_files(files_to_delete)

    print(f"syncing from {source} to {destination}...")
    if sync(source, destination).returncode == 0:
        print("done!")
    else:
        print("error, see session log for details!")


if __name__ == '__main__':
    main()
