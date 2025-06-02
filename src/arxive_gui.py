# arXive GUI script

import sys
from os.path import expanduser
from arxive_common import *

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QFileDialog,
                               QSizePolicy, QListWidgetItem)
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QAction, QIcon, QTextCursor, QColor, QTextCharFormat
from ui.MainWindow import Ui_MainWindow


# Custom class to redirect console output
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
        self.source, self.destination, self.config = None, None, None
        self.listdelButton.setFocus()

        # Redirect console output
        self.output_redirector = OutputRedirector(self.consoleOutput)
        sys.stdout = self.output_redirector
        sys.stderr = self.output_redirector

        # ----- TOOLBAR -----

        # Spacer for buttons
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set source
        source_action = QAction(QIcon('src/ui/source.svg'), "Add source", self)
        source_action.triggered.connect(lambda: self.set_folder("source"))
        self.toolbar.addAction(source_action)

        # Set destination
        destination_action = QAction(
            QIcon('src/ui/destination.svg'), "Add destination", self)
        destination_action.triggered.connect(
            lambda: self.set_folder("destination"))
        self.toolbar.addAction(destination_action)

        # <--- left side
        self.toolbar.addWidget(spacer)
        # right side --->

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

    # -----------------
    # ----- SLOTS -----
    # -----------------

    # ----- TOOLBAR -----

    @Slot()  # Set source/destination
    def set_folder(self, folder):
        folder_path = QFileDialog.getExistingDirectory(
            parent=self, caption=f"Select {folder}", dir=expanduser("~"))
        if folder_path:
            if folder == "source":
                self.source = folder_path
                self.sourceEdit.setText(folder_path)
            else:
                self.destination = folder_path
                self.destEdit.setText(folder_path)
            write_log(f"{folder.capitalize()}: {folder_path}")

    @Slot()  # Configuration
    def config_action(self): print("Configuration...")

    @Slot()   # About
    def about_action(self): print("About...")

    @Slot()  # Exit
    def exit_action(self): sys.exit("Goodbye!")

    # -------------------

    @Slot()
    def list_deletions(self):
        self.statusbar.showMessage("Listing deletions...")
        self.delList.clear()
        try:
            deletions = get_deletions(self.source, self.destination)
            if deletions:
                write_log(f"{len(deletions)} deletions found.")
                for file in deletions:
                    item = QListWidgetItem(file)
                    item.setFlags(item.flags() |
                                  Qt.ItemFlag.ItemIsUserCheckable)
                    item.setCheckState(Qt.CheckState.Unchecked)
                    self.delList.addItem(item)
            else:
                write_log("No deletions found, ready to synchronize.")
            self.statusbar.showMessage("Ready to synchronize.")
            self.syncButton.setEnabled(True)
        except Exception as e:
            # TODO alert
            write_log("Error while listing deletions.", e)
            self.statusbar.showMessage("Deletions could not be listed.")


    @Slot()
    def run_sync(self):

        # Delete files/folders
        entities = [path.join(self.destination, self.delList.item(index).text())
                 for index in range(self.delList.count())
                 if self.delList.item(index).checkState()
                 == Qt.CheckState.Checked]
        for entity in entities:
            try:
                delete_entity(entity)
                write_log(f"{entity} deleted.")
            except Exception as e:
                write_log(f"Error while deleting {entity}!", e)
        write_log(f"{len(entities)} entities deleted.")

        # Synchronize source and destination with rsync
        write_log(f"Syncing from {self.source} to {self.destination}...")
        try:
            self.statusbar.showMessage("Synchronizing...")
            result = sync(self.source, self.destination)
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
            if result.returncode == 0:
                write_log("Synchronization finished.")
                self.statusbar.showMessage("Synchronization finished.")
            else:
                write_log("Error while running rsync!", result.returncode)
        except Exception as e:
            write_log("Error while synchronizing!", e)
        finally:
            self.delList.clear()



# main function
def main():
    """Main function."""

    app = QApplication(sys.argv)
    window = MainWindow()

    # Create session log
    try:
        create_session_log()
    except Exception as e:
        # TODO alert
        write_log(f"Error while creating session log: {e}")
        window.statusbar.showMessage("Session log could not be created.")

    # Load config file
    try:
        window.config = load_config()
        write_log("Configurations loaded.")
    except Exception as e:
        # TODO alert
        write_log("Error while loading configurations!", e)
        window.statusbar.showMessage("Configurations could not be loaded.")

    # Determine source and destination
    window.source, window.destination = None, None
    if len(sys.argv) > 1:
        window.source, window.destination = sys.argv[1], sys.argv[2]
    else:
        window.source = window.config['source']
        window.destination = window.config['destination']
    if not path.exists(window.source):
        # TODO alert
        write_log(f"Warning! Invalid source: {window.source}")
        window.source = None
    else:
        window.sourceEdit.setText(window.source)
    if not path.exists(window.destination):
        # TODO alert
        write_log(f"Warning! Invalid destination: {window.destination}")
        window.destination = None
    else:
        window.destEdit.setText(window.destination)
    window.statusbar.showMessage("Ready.")
    write_log(f"Source: {window.source}\nDestination: {window.destination}")

    # Setting up UI...
    window.show()
    app.exec()


# script body
if __name__ == '__main__':
    main()
