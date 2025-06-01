# arXive CLI script

from sys import argv, exit as close
from arxive_common import *


def main():
    """Main function."""

    # Create session log
    try:
        create_session_log()
    except Exception as e:
        print(f"Error while creating session log: {e}")

    # Load config file
    try:
        config = load_config()
    except Exception as e:
        with open('session.log', 'a', encoding="utf-8") as log:
            log.write(f"Error while loading configurations: {e}")
        close("Error while loading configurations. "
              "See session log for details.")

    # Determine source and destination
    if not path.exists(argv[1]) or not path.exists(argv[2]):
        close("Invalid source/destination!")
    source, destination = argv[1], argv[2]
    print(f"Source: {source}\nDestination: {destination}")

    # Get the list of files deleted from source
    try:
        deletions = get_deletions(source, destination)
    except Exception as e:
        deletions = None
        with open('session.log', 'a', encoding="utf-8") as log:
            log.write(f"Error while listing deletions: {e}")
        close("Error while listing deletions. See session log for details.")

    # Prompt the user for deletions and delete files/folders
    print(f"\n{len(deletions)} file(s)/folder(s) to delete.\n")
    if len(deletions) > 0:
        for entity in deletions:
            print(f"  {entity}")
        choice = input("\nDelete [a]ll, [n]one or "
                       "prompt for each (default)? : ").strip().lower()
        if choice == "a":
            entities = [path.join(destination, file) for file in deletions]
            for entity in entities:
                try:
                    delete_entity(entity)
                except Exception as e:
                    print(f"Error - {e}")
                    with open('session.log', 'a', encoding="utf-8") as log:
                        log.write(f"Error - {e}")
            print(f"{len(entities)} file(s)/folder(s) deleted.\n")
        elif choice == "n":
            print(f"Deletion of {len(deletions)} file(s)/folder(s) skipped.\n")
        else:
            entities = [path.join(destination, entity) for entity in deletions
                        if input(f"Delete {path.join(destination, entity)} "
                                 f"[Y/n]: ").strip().lower() != "n"]
            for entity in entities:
                try:
                    delete_entity(entity)
                except Exception as e:
                    print(f"Error - {e}")
                    with open('session.log', 'a', encoding="utf-8") as log:
                        log.write(f"Error - {e}")
            print(f"{len(entities)} file(s)/folder(s) deleted.\n")

    # Synchronize source and destination with rsync
    choice = input("Proceed with synchronization? [Y/n]: ").strip().lower()
    if choice == "n":
        close("\nSynchronization stopped. Goodbye!")
    else:
        print(f"Syncing from {source} to {destination}...")
        try:
            result = sync(source, destination)
            if result.returncode == 0:
                print("\nSynchronization finished. Goodbye!")
            else:
                print("Rsync error, see session log for details!")
                with open('session.log', 'a', encoding="utf-8") as log:
                    log.write(f"Rsync error: {result.returncode}")
        except Exception as e:
            print(f"Error while synchronizing: {e}")
            with open('session.log', 'a', encoding="utf-8") as log:
                log.write(f"Error while synchronizing: {e}")


if __name__ == '__main__':
    main()
