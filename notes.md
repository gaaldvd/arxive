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

## options

### default:

--archive, -a            archive mode is -rlptgoD (no -A,-X,-U,-N,-H)
--verbose, -v            increase verbosity
