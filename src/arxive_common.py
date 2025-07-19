"""
arXive: A simple CLI/GUI frontend for rsync.

    Copyright (C) 2024  David Gaal (gaaldavid@tuta.io)

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

Check the documentation for details: https://arxive.readthedocs.io
"""

from json import load, dump
from subprocess import run
from os import path, remove, rmdir
from datetime import datetime
from os.path import expanduser

from PySide6.QtWidgets import QFileDialog


def validate_options(options):
    """Check if -a or -v (which are default) is set as additional options.

    :param list options: The list which contains the additional rsync options.

    :return: The validated list of rsync options.
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

    dir_path = QFileDialog.getExistingDirectory(
        parent=parent, caption=f"Select {directory}", dir=expanduser("~"))
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

    The configuration file (JSON) and the dictionary has the following format:

    .. code-block:: json

        {
            "source": "/path/to/source",
            "destination": "/path/to/destination",
            "options": ["--progress", "-l"]
        }

    Attributes:
        config_path (str): The path to the JSON file containing configurations.

        cfg_file (dict): Deserialized data from the `config_path`.

        source (str): The source directory.

        destination (str): The destination directory.

        options (list): Additional options passed to the rsync command.

    Methods:
        load():
            Loads configurations.

        save():
            Saves configurations set by the user.
    """

    config_path = path.expanduser('~/.config/arxive')

    def __init__(self):
        # TODO specify as self.cfg_file
        self.cfg_file = self.load()
        self.source = self.cfg_file['source']
        self.destination = self.cfg_file['destination']
        self.options = self.cfg_file['options']

    def load(self):
        """Load configurations from `cfg_file`.

        :return: The dictionary with the loaded configurations.
        :rtype: dict

        :raises FileNotFoundError: If `cfg_file` cannot be found.
        """

        if path.exists(self.config_path):
            with open(self.config_path, 'r', encoding="utf-8") as file:
                return load(file)
        else:
            raise FileNotFoundError("Configuration file cannot be found at "
                                    "~/.config/arxive.")

    def save(self):
        """Save configurations to the arXive config (JSON) file."""
        with open(self.config_path, 'w', encoding="utf-8") as file:
            config = {"source": self.source, "destination": self.destination,
                      "options": self.options}
            dump(config, file)


class Session:
    """Handles the arXive session.

    Attributes:
        log_path (str): The path to the session log (arXive installation folder).

        source (str): The source directory.

        destination (str): The destination directory.

        options (list): Additional options passed to the rsync command.

        deletions (list): The list of deletions.

        deleted (int): The number of deleted entities.

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
        :param Exception or int exception: Exception forwarded with the message.
        """

        print(msg)
        if exception:
            msg = f"{msg} - {exception}"
        with open(self.log_path, 'a', encoding="utf-8") as log:
            log.write(f"{msg}\n")

    def get_deletions(self):
        """List the files and directories that have been deleted from `source`
        but are still present on `destination`.

        :return: The list of the paths of deleted entities.
        :rtype: list
        """

        cmd = ["rsync", "-av", "--delete", "--dry-run",
               self.source, self.destination]
        deletions = []
        # TODO subprocess.run used without explicitly defining the value for 'check'
        result = run(cmd, capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if line.startswith("deleting "):
                filepath = line[len("deleting "):].strip()
                deletions.append(filepath)
        return deletions

    def delete_entity(self, entity_path):
        """Delete entities in the `Session.deletions` list
        returned by `Session.get_deletions`.

        :param str entity_path: The full path to the entity to be deleted.

        :raises FileNotFoundError: If the entity to be deleted cannot be found.
        """
        if path.isfile(entity_path):
            remove(entity_path)
            self.deleted += 1
        elif path.isdir(entity_path):
            rmdir(entity_path)
            self.deleted += 1
        else:
            # TODO specify FileNotFoundError exception
            raise Exception(f"Error: {entity_path} could not be deleted.")

    def sync(self):
        """Run rsync to synchronize `Session.source` with `Session.destination`.

        :return: The result of the `subprocess.run` method.
        :rtype: subprocess.CompletedProcess
        """
        cmd = ["rsync", "-av"]
        if self.options:
            for option in self.options:
                cmd.append(option)
        cmd.extend([self.source, self.destination])
        # return run(cmd, text=True, capture_output=True)
        # TODO subprocess.run used without explicitly defining the value for 'check'
        return run(cmd, text=True)
