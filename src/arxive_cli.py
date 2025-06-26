# arXive CLI script

from sys import argv, exit as close
from arxive_common import *


def main():
    """Main function."""

    # Create session log
    # try:
    #     create_session_log()
    # except Exception as e:
    #     print(f"Error while creating session log: {e}")

    try:
        session = Session()
    except Exception as e:
        print(f"Error while creating session log: {e}")
        session = None
        close("Goodbye!")

    # Load config file
    # try:
    #     config = load_config()
    # except Exception as e:
    #     write_log("Error while loading configurations!", e)
    #     config = None
    #     close("Goodbye!")

    try:
        config = Config()
    except Exception as e:
        session.log("Error while loading configurations!", e)
        config = None
        close("Goodbye!")

    # Determine source and destination
    # if not (path.exists(argv[1]) or path.exists(argv[2])):
    #     write_log("Error: Invalid source or destination!")
    #     close("Goodbye!")
    # source, destination = argv[1], argv[2]
    # write_log(f"Source: {source}\nDestination: {destination}")

    if not (path.exists(argv[1]) or path.exists(argv[2])):
        session.log("Error: Invalid source or destination!")
        close("Goodbye!")
    session.source, session.destination = argv[1], argv[2]
    session.log(f"Source: {session.source}\nDestination: {session.destination}")

    # Get the list of files deleted from source
    # try:
    #     write_log("Listing deletions...")
    #     deletions = get_deletions(source, destination)
    # except Exception as e:
    #     deletions = None
    #     write_log("Error while listing deletions!", e)
    #     close("Goodbye!")

    try:
        session.log("Listing deletions...")
        session.deletions = session.get_deletions()
    except Exception as e:
        session.deletions = None
        session.log("Error while listing deletions!", e)
        close("Goodbye!")

    # Prompt the user for deletions and delete files/folders
    # write_log(f"\n{len(deletions)} deletion(s) found.\n")
    # if len(deletions) > 0:
    #     for entity in deletions:
    #         print(f"  {entity}")
    #     choice = input("\nDelete [a]ll, [n]one or "
    #                    "prompt for each (default)? : ").strip().lower()
    #     if choice == "a":
    #         entities = [path.join(destination, file) for file in deletions]
    #         for entity in entities:
    #             try:
    #                 delete_entity(entity)
    #                 write_log(f"{entity} deleted.")
    #             except Exception as e:
    #                 write_log(f"Error while deleting {entity}!", e)
    #         write_log(f"{len(entities)} entities deleted.")
    #     elif choice == "n":
    #         write_log(f"Deletion of {len(deletions)} entities skipped.")
    #     else:
    #         entities = [path.join(destination, entity) for entity in deletions
    #                     if input(f"Delete {path.join(destination, entity)} "
    #                              f"[Y/n]: ").strip().lower() != "n"]
    #         for entity in entities:
    #             try:
    #                 delete_entity(entity)
    #             except Exception as e:
    #                 write_log(f"Error while deleting {entity}!", e)
    #         write_log(f"{len(entities)} entities deleted.")

    session.log(f"\n{len(session.deletions)} deletion(s) found.\n")
    if len(session.deletions) > 0:
        for entity in session.deletions:
            print(f"  {entity}")
        choice = input("\nDelete [a]ll, [n]one or "
                       "prompt for each (default)? : ").strip().lower()
        if choice == "a":
            entities = [path.join(session.destination, file)
                        for file in session.deletions]
            for entity in entities:
                try:
                    session.delete_entity(entity)
                    session.log(f"{entity} deleted.")
                except Exception as e:
                    session.log(f"Error while deleting {entity}!", e)
            session.log(f"{session.deleted} entities deleted.")
        elif choice == "n":
            session.log(f"Deletion of {len(session.deletions)} "
                        f"entities skipped.")
        else:
            entities = [path.join(session.destination, entity)
                        for entity in session.deletions
                        if input(f"Delete "
                                 f"{path.join(session.destination, entity)} "
                                 f"[Y/n]: ").strip().lower() != "n"]
            for entity in entities:
                try:
                    session.delete_entity(entity)
                    session.log(f"{entity} deleted.")
                except Exception as e:
                    session.log(f"Error while deleting {entity}!", e)
            session.log(f"{session.deleted} entities deleted.")

    # Synchronize source and destination with rsync
    # choice = input("\nProceed with synchronization? [Y/n]: ").strip().lower()
    # if choice == "n":
    #     write_log("\nSynchronization stopped. Goodbye!")
    #     close("Goodbye!")
    # else:
    #     write_log(f"Syncing from {source} to {destination}...")
    #     try:
    #         result = sync(source, destination, config.options)
    #         if result.returncode == 0:
    #             write_log("\nSynchronization finished. Goodbye!")
    #         else:
    #             write_log("Error while running rsync!", result.returncode)
    #     except Exception as e:
    #         write_log("Error while synchronizing!", e)

    choice = input("\nProceed with synchronization? [Y/n]: ").strip().lower()
    if choice == "n":
        session.log("\nSynchronization stopped. Goodbye!")
        close("Goodbye!")
    else:
        session.log(f"Syncing from {session.source} "
                    f"to {session.destination}...")
        try:
            result = session.sync()
            if result.returncode == 0:
                session.log("\nSynchronization finished. Goodbye!")
            else:
                session.log("Error while running rsync!",
                            result.returncode)
        except Exception as e:
            session.log("Error while synchronizing!", e)


if __name__ == '__main__':
    main()
