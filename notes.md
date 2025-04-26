# arxive notes

rsync man: https://download.samba.org/pub/rsync/rsync.1

- session
  - mount up NAS, ask if it should be unmounted at the end of the session (optional) 
  - define SOURCE and DESTINATION
- rsync --delete --dry-run SOURCE to DESTINATION
  - list files in DESTINATION that have been removed from SOURCE
    - prompt for the removal of each file from DESTINATION (checks in Qt)
    - delete files marked for removal
- rsync SOURCE to DESTINATION

## setting up & usage

requirements: git, python3, pipenv, rsync

1. clone git repo: `git clone https://github.com/gaaldvd/arxive.git`
2. cd to the repo and run setup script: `sh setup.sh`
3. add arxive.sh to PATH:
- create `.profile` file in home
- add the line `export PATH="/home/USER/PATH/TO/ARXIVE:$PATH"` to the file
- reload configuration: `source ~/.profile`
- verify: `echo $PATH`
- create symlink: `ln -s /home/USER/PATH/TO/ARXIVE/arxive.sh /home/USER/PATH/TO/ARXIVE/arxive`

update: `arxive -u`

run in CLI or GUI mode: `arxive -c/-g [SOURCE] [DESTINATION]`

## template

```python
import subprocess
import os
import shlex

# === CONFIG ===
SOURCE = "source/"
DESTINATION = "destination/"  # Ensure trailing slashes as needed

# === Run rsync dry-run to find files to delete ===
def get_deletions():
    cmd = ["rsync", "-av", "--delete", "--dry-run", SOURCE, DESTINATION]
    result = subprocess.run(cmd, capture_output=True, text=True)
    deletions = []
    for line in result.stdout.splitlines():
        if line.startswith("deleting "):
            filepath = line[len("deleting "):].strip()
            deletions.append(filepath)
    return deletions

# === Prompt user for each file and delete if confirmed ===
def prompt_and_delete(files):
    for file in files:
        full_path = os.path.join(DESTINATION, file)
        print(f"\nFile to delete: {full_path}")
        choice = input("Delete this file? [y/N]: ").strip().lower()
        if choice == "y":
            try:
                os.remove(full_path)
                print(f"Deleted: {full_path}")
            except Exception as e:
                print(f"Error deleting {full_path}: {e}")
        else:
            print(f"Skipped: {full_path}")

def main():
    files_to_delete = get_deletions()
    if not files_to_delete:
        print("No files to delete.")
    else:
        print(f"{len(files_to_delete)} files marked for deletion.")
        prompt_and_delete(files_to_delete)

if __name__ == "__main__":
    main()
```

### notes

- This script assumes that the destination files exist exactly where rsync would delete them.
- You might want to add support for directories (os.rmdir) or use shutil.rmtree() if you expect folders too.
- If your file names contain spaces or special characters, this handles them correctly using Python strings.
