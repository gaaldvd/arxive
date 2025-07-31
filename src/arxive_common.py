"""
arXive: A simple CLI/GUI frontend for rsync.

This file contains the code for the shared functions and classes of arXive.

Check the documentation for details: https://arxive.readthedocs.io

    Copyright (C) 2025 David Gaal (gaaldvd@proton.me)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from json import load, dump
from subprocess import run, CalledProcessError
from os import path, remove, rmdir
from datetime import datetime
from os.path import expanduser

from PySide6.QtWidgets import QFileDialog


def validate_options(options):
    """Check if -a or -v (which are default) is set as additional options.

    :param list options: Additional rsync options (usually from
        :ref:`Session.options <session-class>` or
        :ref:`Config.options <config-class>`).

    :return: Validated list of rsync options.
    :rtype: list
    """

    if options:
        if bool(set(options) & {"-av", "--archive", "-a", "--verbose", "-v"}):
            print("Warning: --archive (-a) and --verbose (-v) "
                  "are default options (-av)!")
            options = [option for option in options
                              if option not in ("-av", "--archive",
                                                "-a", "--verbose", "-v")]
    return options

def set_dir(parent, directory):
    """Set a directory chosen by the user in a dialog window.

    :param MainWindow or ConfigDialog parent: The window from which
        the dialog is opened.
    :param str directory: The type of the directory (source or destination).
    """

    # Opening a dialog for choosing the directory
    dir_path = QFileDialog.getExistingDirectory(
        parent=parent, caption=f"Select {directory}", dir=expanduser("~"))

    # If the parent is the main window the 'Run sync' button is disabled and the
    # directories get validated when the 'List deletions' button is pressed
    if dir_path:
        if parent.objectName() == "MainWindow":
            parent.syncButton.setEnabled(False)
        if directory == "source":
            parent.sourceEdit.setText(dir_path)
            if parent.objectName() == "MainWindow":
                parent.session.log(f"{directory.capitalize()}: {dir_path}")
        else:
            parent.destEdit.setText(dir_path)
            if parent.objectName() == "MainWindow":
                parent.session.log(f"{directory.capitalize()}: {dir_path}")


class Config:
    """Handles the configurations set by the user.

    The configuration file (`config_path`) and the dictionary (`config_data`)
    has the following format:

    .. code-block:: json

        {
            "source": "/path/to/source",
            "destination": "/path/to/destination",
            "options": ["--progress", "-l"]
        }

    :ivar str config_path: The path to the JSON file with the configurations.
    :ivar dict config_data: Deserialized data from the `config_path` file.
    :ivar str source: The source directory.
    :ivar str destination: The destination directory.
    :ivar list options: Additional options passed to the rsync command.

    Methods:
        load():
            Loads configurations.

        save():
            Saves configurations.
    """

    # Default config directory on most Linux distributions
    config_path = path.expanduser('~/.config/arxive')

    def __init__(self):
        self.config_data = self.load()
        self.source = self.config_data['source']
        self.destination = self.config_data['destination']
        self.options = self.config_data['options']

    def load(self):
        """Load configurations from `config_path`.

        :return: Deserialized configurations data.
        :rtype: dict

        :raises FileNotFoundError: If `config_path` cannot be found.
        """

        # Validating the config file which is created when the app is installed
        if path.exists(self.config_path):
            with open(self.config_path, 'r', encoding="utf-8") as file:

                # Returning deserialized JSON data
                return load(file)
        else:
            raise FileNotFoundError("Configuration file cannot be found at "
                                    "~/.config/arxive.")

    def save(self):
        """Save configurations to `config_path`."""

        # There is no need to validate the path since `load` is called
        # when the app is initialized, and it would raise an exception
        # if the file was missing
        with open(self.config_path, 'w', encoding="utf-8") as file:
            config = {"source": self.source, "destination": self.destination,
                      "options": self.options}

            # Serializing dictionary to JSON data
            dump(config, file)


class Session:
    """Handles an arXive session.

    :ivar str log_path: The path to the session log.
    :ivar str source: The source directory.
    :ivar str destination: The destination directory.
    :ivar list options: Additional options passed to the rsync command.
    :ivar list deletions: The list of files/directories deleted from `source`.

    Methods:
        init_log():
            Initializes the session log.

        log(msg, exception=None):
            Writes messages to the standard output and the session log.

        get_deletions():
            Lists deletions from the source.

        delete_entity(entity_path):
            Deletes a file or directory.

        sync():
            Runs rsync to synchronize the source with the destination.
    """

    # arXive installation folder
    log_path = (f"{path.dirname(path.dirname(path.abspath(__file__)))}"
                f"/session.log")

    def __init__(self):
        self.init_log()
        self.source = None
        self.destination = None
        self.options = None
        self.deletions = None
        self.deleted = None

    def init_log(self):
        """Initialize the session log in the installation folder."""

        with open(self.log_path, 'w', encoding="utf-8") as log:
            log.write(f"=============================================\n"
                      f"arXive session log -- "
                      f"{datetime.now().strftime("%Y %b %d. - %X")}\n"
                      f"=============================================\n")

    def log(self, msg, exception=None):
        """Print messages and status updates to the standard output
        and write them into the session log.

        :param str msg: The message to print.
        :param Exception or int exception: Exception or `subprocess.run` result
            code forwarded with the message.
        """

        print(msg)

        # If there is an `exception` it gets attached to the message
        # and written into the session log
        if exception:
            msg = f"{msg} - {exception}"
        with open(self.log_path, 'a', encoding="utf-8") as log:
            log.write(f"{msg}\n")

    def get_deletions(self):
        """List the files and directories that have been deleted from `source`
        but are still present on `destination`.

        :return: The paths of deleted entities.
        :rtype: list
        """

        # Doing a dry-run of `rsync --delete` and catching the output
        cmd = ["rsync", "-av", "--delete", "--dry-run",
               self.source, self.destination]
        deletions = []
        try:
            result = run(cmd, capture_output=True, text=True, check=True)
        except CalledProcessError as e:
            return e

        # Extracting the list of deletions from the output
        for line in result.stdout.splitlines():
            if line.startswith("deleting "):
                filepath = line[len("deleting "):].strip()
                deletions.append(filepath)

        # Returning the list of extracted paths
        return deletions

    def delete_entity(self, entity_path):
        """Delete an file or directory from the `deletions` list
        returned by `get_deletions`.

        :param str entity_path: The full path of the entity.

        :raises FileNotFoundError: If `entity_path` cannot be found.
        """

        # Checking whether the entity is a file or a directory and deleting it
        if path.isfile(entity_path):
            remove(entity_path)
            self.deleted += 1
        elif path.isdir(entity_path):
            rmdir(entity_path)
            self.deleted += 1
        else:
            raise FileNotFoundError(f"Error: {entity_path}"
                                    f" could not be deleted.")

    def sync(self):
        """Run rsync to synchronize `source` with `destination`.

        :return: The result object of the `subprocess.run` method.
        :rtype: subprocess.CompletedProcess
        """

        cmd = ["rsync", "-av"]

        # Attaching additional options if there are any
        if self.options:
            for option in self.options:
                cmd.append(option)

        # Attaching source and destination
        cmd.extend([self.source, self.destination])

        # Running rsync and returning the result object
        return run(cmd, text=True, check=True)
