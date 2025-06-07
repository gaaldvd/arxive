# arxive notes

rsync man: https://download.samba.org/pub/rsync/rsync.1

## setting up & usage

requirements: git, python3, pipenv, rsync

1. clone git repo: `git clone https://github.com/gaaldvd/arxive.git`
2. cd to the repo and run setup script: `sh setup.sh`

update: `arxive -u`

run in CLI or GUI mode: `arxive -c/-g [SOURCE] [DESTINATION]`

## options

### default:

--archive, -a            archive mode is -rlptgoD (no -A,-X,-U,-N,-H)
--verbose, -v            increase verbosity
