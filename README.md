# arXive

**A simple CLI/GUI frontend for [rsync](https://rsync.samba.org/).**

## Installation

*Requirements*: git, python3, pipenv, rsync

1. Open a terminal in the directory where you want to install the application (e.g. `~/bin`)
2. Clone the repository: `git clone https://github.com/gaaldvd/arxive.git`
3. Run the setup script: `sh setup.sh`

## Usage

The main feature of the application (besides serving as a frontend) is that it enables the user to choose which files/directories to delete from the destination if they're missing from the source (native rsync can be used with the --delete option which deletes *all* the missing files/directories). 

### CLI

### GUI

## Update

1. Start the application from the terminal with the -u option: `arxive -u`
2. Follow the prompts to update the environment and/or the repository

There is also an Update button on the GUI toolbar.

## Errors

Any error can be reported through [e-mail](mailto:gaaldvd[at]proton.me?subject=[GitHub]%20arXive%20error) with the exact error message and/or screenshot. Alternatively, an [issue](https://github.com/gaaldvd/arxive/issues) can be opened.
