# arXive GUI script

import sys
from os.path import expanduser

from arxive_common import *
from arxive_gui_dialogs import *

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QFileDialog,
                               QSizePolicy, QListWidgetItem)
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QAction, QIcon, QTextCursor, QColor, QTextCharFormat
from ui.MainWindow import Ui_MainWindow


def set_dir(parent, directory):
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


class OutputRedirector:
    def __init__(self, plain_text_edit):
        self.plain_text_edit = plain_text_edit

    def write(self, text):
        if text.strip():  # Avoid empty lines
            # Determine color based on content
            if "error" in text.lower():
                color = QColor("red")
            elif "warning" in text.lower():
                color = QColor("orange")
            elif any(keyword in text.lower() for keyword in
                     ["ready", "finished", "saved"]):
                color = QColor("green")
            else:
                color = QColor("black")

            # Append text with the determined color
            self.append_colored_text(text.strip(), color)

    def flush(self):
        pass  # Required for compatibility with `sys.stdout`

    def append_colored_text(self, text, color):
        # Move cursor to the end
        cursor = self.plain_text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)

        # Set text format
        text_format = QTextCharFormat()
        text_format.setForeground(color)

        # Insert text with the format
        cursor.insertText(text + "\n", text_format)

        # Ensure the cursor remains at the end
        self.plain_text_edit.setTextCursor(cursor)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.session = None
        self.config = None
        self.listdelButton.setFocus()

        # Redirecting console output
        self.output_redirector = OutputRedirector(self.consoleOutput)
        sys.stdout = self.output_redirector
        sys.stderr = self.output_redirector

        # ----- TOOLBAR -----

        # Spacer for buttons
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set source
        source_action = QAction(QIcon('src/ui/source.svg'), "Add source", self)
        source_action.triggered.connect(
            lambda: set_dir(self, "source"))
        self.toolbar.addAction(source_action)

        # Set destination
        destination_action = QAction(
            QIcon('src/ui/destination.svg'), "Add destination", self)
        destination_action.triggered.connect(
            lambda: set_dir(self, "destination"))
        self.toolbar.addAction(destination_action)

        # Use defaults
        defaults_action = QAction(QIcon('src/ui/defaults.svg'),
                                  "Use defaults", self)
        defaults_action.triggered.connect(self.defaults_action)
        self.toolbar.addAction(defaults_action)

        # <--- left side
        self.toolbar.addWidget(spacer)
        # right side --->

        # Update
        update_action = QAction(
            QIcon('src/ui/update.svg'), "Update", self)
        update_action.triggered.connect(self.update_action)
        self.toolbar.addAction(update_action)

        # Configuration
        config_action = QAction(
            QIcon('src/ui/configure.svg'), "Configuration", self)
        config_action.triggered.connect(self.config_action)
        self.toolbar.addAction(config_action)

        # About
        about_action = QAction(QIcon('src/ui/help-about.svg'), "About", self)
        about_action.triggered.connect(self.about_action)
        self.toolbar.addAction(about_action)

        # Exit
        exit_action = QAction(QIcon('src/ui/window-close.svg'), "Exit", self)
        exit_action.triggered.connect(self.exit_action)
        self.toolbar.addAction(exit_action)

        # -------------------

        self.listdelButton.clicked.connect(self.list_deletions)
        self.syncButton.clicked.connect(self.run_sync)
        self.delallRadio.clicked.connect(self.mark_all)

    # -----------------
    # ----- SLOTS -----
    # -----------------

    # ----- TOOLBAR -----

    @Slot()
    def defaults_action(self):
        self.sourceEdit.setText(self.config.source)
        self.destEdit.setText(self.config.destination)
        self.session.options = self.config.options
        self.session.log(f"Source: {self.sourceEdit.text()}\n"
                         f"Destination: {self.destEdit.text()}")
        if self.session.options:
            self.session.log(f"Additional options: "
                             f"{", ".join(self.session.options)}")
        self.syncButton.setEnabled(False)

    @Slot()
    def update_action(self): print("Updating...")

    @Slot()  # Configuration
    def config_action(self):
        dialog = ConfigDialog(self.config)
        dialog.config_updated.connect(self.config_updated)
        dialog.exec()

    @Slot()
    def config_updated(self):
        self.config = Config()

        # Validating source
        if not path.exists(self.config.source):
            self.session.log(f"Warning! Invalid source: {self.config.source}")

        # Validating destination
        if not path.exists(self.config.destination):
            self.session.log(f"Warning! Invalid destination: "
                             f"{self.config.destination}")

    @Slot()   # About
    def about_action(self):
        dialog = AboutDialog(self)
        dialog.exec()

    @Slot()  # Exit
    def exit_action(self): sys.exit("Goodbye!")

    # -------------------

    @Slot()
    def mark_all(self):
        for index in range(self.delList.count()):
            self.delList.item(index).setCheckState(Qt.CheckState.Checked)

    @Slot()
    def list_deletions(self):
        self.session.source = self.sourceEdit.text()
        self.session.destination = self.destEdit.text()
        if (path.exists(self.session.source)
                and path.exists(self.session.destination)
                and self.session.source != self.session.destination):
            try:
                self.statusbar.showMessage("Listing deletions...")
                deletions = self.session.get_deletions()
                if deletions:
                    self.session.log(f"{len(deletions)} deletion(s) found, "
                                     f"ready to synchronize.")
                    self.delallRadio.setEnabled(True)
                    for file in deletions:
                        item = QListWidgetItem(file)
                        item.setFlags(item.flags() |
                                      Qt.ItemFlag.ItemIsUserCheckable)
                        item.setCheckState(Qt.CheckState.Unchecked)
                        self.delList.addItem(item)
                else:
                    self.session.log("No deletions found, "
                                     "ready to synchronize.")
                self.statusbar.showMessage("Ready to synchronize.")
                self.syncButton.setEnabled(True)
            except Exception as e:
                self.session.log("Error while listing deletions!", e)
                self.statusbar.showMessage("Deletions could not be listed.")
        else:
            if not path.exists(self.session.source):
                self.session.log("Error: Invalid source!")
            if not path.exists(self.session.destination):
                self.session.log("Error: Invalid destination!")
            if self.session.source == self.session.destination:
                self.session.log("Error: Source and destination "
                                 "must be different!")

    @Slot()
    def run_sync(self):

        # Deleting files/directories
        entities = [path.join(self.session.destination,
                              self.delList.item(index).text())
                    for index in range(self.delList.count())
                    if self.delList.item(index).checkState()
                    == Qt.CheckState.Checked]
        self.session.deleted = 0
        for entity in entities:
            try:
                self.session.delete_entity(entity)
                self.session.deleted += 1
                self.session.log(f"{entity} deleted.")
            except Exception as e:
                self.session.log(f"Error while deleting {entity}!", e)
        self.session.log(f"{self.session.deleted} entities deleted.")

        # Synchronizing source and destination with rsync
        self.session.log(f"Syncing from {self.session.source} "
                         f"to {self.session.destination}...")
        try:
            self.statusbar.showMessage("Synchronizing...")
            result = self.session.sync()
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
            if result.returncode == 0:
                self.session.log("Synchronization finished.")
                self.statusbar.showMessage("Synchronization finished.")
            else:
                self.session.log("Error while running rsync!",
                                 result.returncode)
        except Exception as e:
            self.session.log("Error while synchronizing!", e)
        finally:
            self.delList.clear()
            self.delallRadio.setChecked(False)
            self.delallRadio.setEnabled(False)
            self.syncButton.setEnabled(False)


# main function
def main():
    """Main function."""

    app = QApplication(sys.argv)
    window = MainWindow()

    # Creating session log
    try:
        window.session = Session()
        window.session.log("Session log created.")
    except Exception as e:
        print(f"Error while creating session log: {e}")
        window.session = None

    # Loading config file
    try:
        window.config = Config()
        window.session.log("Configurations loaded.")
    except Exception as e:
        window.session.log("Error while loading configurations!", e)
        window.statusbar.showMessage("Configurations could not be loaded.")

    # Setting source, destination and options
    try:
        if len(sys.argv[1]) > 0 and len(sys.argv[2]) > 0:
            window.session.source = sys.argv[1]
            window.session.destination = sys.argv[2]
        else:
            window.session.source = window.config.source
            window.session.destination = window.config.destination

        window.sourceEdit.setText(window.session.source)
        window.destEdit.setText(window.session.destination)

        window.session.options = window.config.options

        if window.session.source != "":
            window.session.log(f"Source: {window.session.source}")
        if window.session.destination != "":
            window.session.log(f"Destination: {window.session.destination}")
        if window.session.options:
            window.session.log(f"Additional options: "
                               f"{", ".join(window.session.options)}")

        window.statusbar.showMessage("Ready.")
    except Exception as e:
        window.session.log(f"Error while initiating application!", e)

    # Setting up UI...
    window.show()
    app.exec()


# script body
if __name__ == '__main__':
    main()
