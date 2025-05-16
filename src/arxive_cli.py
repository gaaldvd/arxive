# arXive CLI script

from sys import argv
from arxive_common import *


def prompt_deletions(files, destination):
    files_to_delete = []
    for file in files:
        full_path = path.join(destination, file)
        print(full_path)
        choice = input("delete? [y/N]: ").strip().lower()
        if choice == "y":
            files_to_delete.append(full_path)
    return files_to_delete


# main function
def main():
    """Main function."""

    config = load_config()
    print(f"configs: {config}")

    if len(argv) > 1:
        source, destination = argv[1], argv[2]
    elif config['source'] and config['destination']:
        source, destination = config['source'], config['destination']
    else:
        source, destination = input("source: "), input("destination: ")
        choice = input("save as default? [y/N]: ").strip().lower()
        if choice == "y":
            save_config({'source': source, 'destination': destination})

    print(f"source: {source}\ndestination: {destination}")

    deletions = get_deletions(source, destination)
    print(f"deletions: {deletions}")

    files_to_delete = prompt_deletions(deletions, destination)
    print(f"files to delete: {files_to_delete}")

    delete_files(files_to_delete)


# script body
if __name__ == '__main__':
    main()
