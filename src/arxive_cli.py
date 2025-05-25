# arXive CLI script

from sys import argv, exit as close
from arxive_common import *


def main():
    """Main function."""

    # Create session log, load config file
    create_session_log()
    config = load_config()
    if config is False:
        close("Error, see session log for details!")

    # Determine source and destination
    if not path.exists(argv[1]) or not path.exists(argv[2]):
        close("Invalid source/destination!")
    source, destination = argv[1], argv[2]
    print(f"Source: {source}\nDestination: {destination}")

    # Get the list of files deleted from source
    deletions = get_deletions(source, destination)
    if deletions is False:
        close("Error, see session log for details!")

    # Prompt the user for which files to delete and delete files
    print(f"\n{len(deletions)} file(s) to delete.\n")
    if len(deletions) > 0:
        for file in deletions:
            print(f"  {file}")
        choice = input("\nDelete [a]ll, [n]one or "
                       "prompt for each (default)? : ").strip().lower()
        if choice == "a":
            files_to_del = [path.join(destination, file) for file in deletions]
            if delete_files(files_to_del) is False:
                close("Error, see session log for details!")
            print(f"{len(files_to_del)} file(s) deleted.\n")
        elif choice == "n":
            print(f"Deletion of {len(deletions)} file(s) skipped.\n")
        else:
            files_to_del = [path.join(destination, file) for file in deletions
                            if input(f"Delete {path.join(destination, file)}"
                                     f" [Y/n]: ").strip().lower() != "n"]
            if delete_files(files_to_del) is False:
                close("Error, see session log for details!")
            print(f"{len(files_to_del)} file(s) deleted.\n")

    # Synchronize source and destination with rsync
    choice = input("Proceed with synchronization? [Y/n]: ").strip().lower()
    if choice == "n":
        close("\nSynchronization stopped. Goodbye!")
    else:
        print(f"Syncing from {source} to {destination}...")
        if sync(source, destination).returncode == 0:
            print("\nSynchronization finished. Goodbye!")
        else:
            print("Error, see session log for details!")


if __name__ == '__main__':
    main()
