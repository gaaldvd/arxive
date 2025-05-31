# arXive GUI script

import sys
from os.path import expanduser
from arxive_common import *

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QFileDialog,
                               QSizePolicy, QListWidgetItem)
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QAction, QIcon, QTextCursor
from ui.MainWindow import Ui_MainWindow


# Custom class to redirect console output
class OutputRedirector:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, text):
        # Append text to the widget
        self.text_edit.moveCursor(QTextCursor.End)  # Move to the end
        self.text_edit.insertPlainText(text)
        self.text_edit.ensureCursorVisible()  # Scroll to the bottom

    def flush(self):
        pass  # No-op for compatibility with sys.stdout requirements


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)
        self.source, self.destination = None, None
        self.listdelButton.setFocus()

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
                self.sourceEdit.setText(folder_path)
            else:
                self.destEdit.setText(folder_path)
            print(f"{folder.capitalize()}: {folder_path}")

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
        deletions = get_deletions(self.source, self.destination)
        print(f"{len(deletions)} deletions found.")
        if deletions is False:
            print("Error, see session log for details!")
        if deletions:
            for file in deletions:
                item = QListWidgetItem(file)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.delList.addItem(item)
            self.statusbar.showMessage("Deletions listed, "
                                       "ready to synchronize.")
        else:
            self.statusbar.showMessage("No deletions found, "
                                       "ready to synchronize.")
        self.syncButton.setEnabled(True)

    @Slot()
    def run_sync(self):
        files = [path.join(self.destination, self.delList.item(index).text())
                 for index in range(self.delList.count())
                 if self.delList.item(index).checkState()
                 == Qt.CheckState.Checked]
        if delete_files(files) is False:
            print("Error, see session log for details!")
        if files:
            print(f"{len(files)} file(s) deleted.")
        print(f"Syncing from {self.source} to {self.destination}...")
        result = sync(self.source, self.destination)
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        if result.returncode == 0:
            self.statusbar.showMessage("Synchronization finished.")
            print("Synchronization finished.")
        else:
            print("Error, see session log for details!")


# main function
def main():
    """Main function."""

    app = QApplication(sys.argv)
    window = MainWindow()

    # Create session log, load config file
    create_session_log()
    config = load_config()
    if config is False:
        # TODO alert
        sys.exit("Error, see session log for details!")

    # Determine source and destination from CLI arguments
    source, destination = None, None
    if len(sys.argv) > 1:
        if not path.exists(sys.argv[1]) or not path.exists(sys.argv[2]):
            # TODO alert
            pass
        else:
            source, destination = sys.argv[1], sys.argv[2]
            window.sourceEdit.setText(source)
            window.destEdit.setText(destination)
            window.statusbar.showMessage("Ready.")

    print(f"Source: {source}\nDestination: {destination}")
    window.source, window.destination = source, destination

    # Setting up UI...
    window.show()
    app.exec()


# script body
if __name__ == '__main__':
    main()
