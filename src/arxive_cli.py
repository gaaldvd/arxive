# arXive CLI script

from sys import argv, exit as close
from arxive_common import *


def main():
    """Main function."""

    # Creating session log
    try:
        session = Session()
        session.log("Session log created.")
    except Exception as e:
        print(f"Error while creating session log: {e}")
        session = None
        close("Goodbye!")

    # Loading config file
    try:
        config = Config()
        session.log("Configurations loaded.")
    except Exception as e:
        session.log("Error while loading configurations!", e)
        config = None
        close("Goodbye!")

    no_interrupt = True if argv[3] == "true" else False

    if no_interrupt:
        session.log("No interruption mode is ACTIVE!")

    # Setting and validating source and destination
    session.source, session.destination = argv[1], argv[2]
    if not session.source or not session.destination:
        session.log("Error: Source and destination must be provided!")
        close("Goodbye!")

    if (path.exists(session.source) and path.exists(session.destination)
            and session.source != session.destination):
        session.log(f"Source: {session.source}\n"
                    f"Destination: {session.destination}")
    else:
        if not path.exists(session.source):
            session.log("Error: Invalid source!")
        if not path.exists(session.destination):
            session.log("Error: Invalid destination!")
        if session.source == session.destination:
            session.log("Error: Source and destination must be different!")
        close("Goodbye!")

    # Listing deletions
    try:
        session.log("Listing deletions...")
        session.deletions = session.get_deletions()
    except Exception as e:
        session.deletions = None
        session.log("Error while listing deletions!", e)
        close("Goodbye!")

    # Prompting the user for deletions and deleting files/directories
    session.log(f"\n{len(session.deletions)} deletion(s) found.\n")
    if len(session.deletions) > 0:
        for entity in session.deletions:
            print(f"  {entity}")
        if no_interrupt:
            del_choice = "a"
        else:
            del_choice = input("\nDelete [a]ll, [n]one or "
                               "prompt for each (default)? : ").strip().lower()
        if del_choice == "a":
            entities = [path.join(session.destination, file)
                        for file in session.deletions]
            session.deleted = 0
            for entity in entities:
                try:
                    session.delete_entity(entity)
                    session.deleted += 1
                    session.log(f"{entity} deleted.")
                except Exception as e:
                    session.log(f"Error while deleting {entity}!", e)
            session.log(f"{session.deleted} entities deleted.")
        elif del_choice == "n":
            session.log(f"Deletion of {len(session.deletions)} "
                        f"entities skipped.")
        else:
            entities = [path.join(session.destination, entity)
                        for entity in session.deletions
                        if input(f"Delete "
                                 f"{path.join(session.destination, entity)} "
                                 f"[Y/n]: ").strip().lower() != "n"]
            session.deleted = 0
            for entity in entities:
                try:
                    session.delete_entity(entity)
                    session.deleted += 1
                    session.log(f"{entity} deleted.")
                except Exception as e:
                    session.log(f"Error while deleting {entity}!", e)
            session.log(f"{session.deleted} entities deleted.")

    # Synchronizing source and destination with rsync
    if no_interrupt:
        sync_choice = "y"
    else:
        sync_choice = input("\nProceed with synchronization? "
                            "[Y/n]: ").strip().lower()
    if sync_choice == "n":
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
