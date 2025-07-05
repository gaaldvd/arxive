# arXive CLI script

from sys import argv, exit as close
from arxive_common import *


def main():
    """Main function."""

    # Create session log
    try:
        create_session_log()
    except Exception as e:
        write_log(f"Error while creating session log: {e}")

    # Load config file
    try:
        config = load_config()
    except Exception as e:
        write_log("Error while loading configurations!", e)
        config = None
        close("Goodbye!")

    # Determine source and destination
    if not (path.exists(argv[1]) or path.exists(argv[2])):
        write_log("Error: Invalid source or destination!")
        close()
    source, destination = argv[1], argv[2]
    write_log(f"Source: {source}\nDestination: {destination}")

    # Get the list of files deleted from source
    try:
        write_log("Listing deletions...")
        deletions = get_deletions(source, destination)
    except Exception as e:
        deletions = None
        write_log("Error while listing deletions!", e)
        close()

    # Prompt the user for deletions and delete files/folders
    write_log(f"\n{len(deletions)} deletion(s) found.\n")
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
                    write_log(f"{entity} deleted.")
                except Exception as e:
                    write_log(f"Error while deleting {entity}!", e)
            write_log(f"{len(entities)} entities deleted.")
        elif choice == "n":
            write_log(f"Deletion of {len(deletions)} entities skipped.")
        else:
            entities = [path.join(destination, entity) for entity in deletions
                        if input(f"Delete {path.join(destination, entity)} "
                                 f"[Y/n]: ").strip().lower() != "n"]
            for entity in entities:
                try:
                    delete_entity(entity)
                except Exception as e:
                    write_log(f"Error while deleting {entity}!", e)
            write_log(f"{len(entities)} entities deleted.")

    # Synchronize source and destination with rsync
    choice = input("\nProceed with synchronization? [Y/n]: ").strip().lower()
    if choice == "n":
        write_log("\nSynchronization stopped. Goodbye!")
        close()
    else:
        write_log(f"Syncing from {source} to {destination}...")
        try:
            result = sync(source, destination, config['options'])
            if result.returncode == 0:
                write_log("\nSynchronization finished. Goodbye!")
            else:
                write_log("Error while running rsync!", result.returncode)
        except Exception as e:
            write_log("Error while synchronizing!", e)


if __name__ == '__main__':
    main()
