# arXive

**A simple CLI/GUI frontend for [rsync](https://rsync.samba.org/).**

The main feature of the application (besides serving as a frontend) is that it enables the user to choose which files/directories to delete from the destination if they're missing from the source (native rsync can be used with the `--delete` option which deletes *all* the missing files/directories).

Developers are welcome to fork this [repository](https://github.com/gaaldvd/arxive).

**Contents:**

- [Installation](#installation)
- [Usage](#usage)
  - [CLI](#cli)
  - [GUI](#gui)
- [Update](#update)
- [Reporting errors](#reporting-errors)
- [Technical reference for developers](https://arxive.readthedocs.io/en/latest/reference.html)

## Installation

*Requirements*: git, python3, pipenv, rsync

1. Open a terminal in the directory where you want to install arXive (e.g. `~/bin`)
2. Clone the repository: `git clone https://github.com/gaaldvd/arxive.git`
3. Run the setup script: `sh setup.sh`

## Usage

### CLI

Start arXive from the terminal with the following command:

`arxive -c|-g|-u [-n] <PATH/TO/SOURCE> <PATH/TO/DESTINATION>`

The `-c` option starts the application in CLI mode (use `-g` for GUI mode) and the optional `-n` toggles no-interruption mode (in this case the script won't prompt the user for anything and all the deletions from the source will be deleted from the destination - so just like rsync with the --del option).

For example: `arxive -c /home/me/here /remote/there`

After this arXive lists the deletions (the files and directories that are deleted from the source but present on the destination) and prompts the user what to do with the these (delete all, none or prompt for each). Finally the synchronization runs and the session is done.

The session log (`session.log` in the installation directory) contains details and error messages.

### GUI

Start arXive from the Application Menu or from the terminal with the `-g` option. There is no no-interruption mode in the GUI mode!

The user interface is self-explanatory. The source and destination directories can be set with the first two buttons on the toolbar, the third one sets the defaults from the configuration file. These defaults can be changed in the configuration dialog which can be opened from the toolbar as well. Use the update button to update the repository and the environment.

After choosing the directories use the List deletions button, tick the files and directories you'd like to delete and Run sync!

## Update

1. Start the application from the terminal with the `-u` option: `arxive -u`
2. Follow the prompts to update the environment and/or the repository

There is also an Update button on the GUI toolbar.

## Reporting errors

Any error can be reported through [e-mail](mailto:gaaldvd[at]proton.me?subject=[GitHub]%20arXive%20error) with the exact error message and/or screenshot. Alternatively, an [issue](https://github.com/gaaldvd/arxive/issues) can be opened.
