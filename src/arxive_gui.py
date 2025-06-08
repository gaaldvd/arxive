# arXive GUI script

import sys
from os.path import expanduser

from arxive_common import *

from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog, QWidget,
                               QFileDialog, QSizePolicy, QListWidgetItem)
from PySide6.QtCore import Slot, Signal, Qt
from PySide6.QtGui import QAction, QIcon, QTextCursor, QColor, QTextCharFormat
from ui.MainWindow import Ui_MainWindow
from ui.About import Ui_Dialog as AboutDlg
from ui.Config import Ui_Dialog as ConfigDlg


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

        self.config = None
        self.source, self.destination, self.options = None, None, None
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
        source_action.triggered.connect(
            lambda: self.set_folder(self, "source", "main"))
        self.toolbar.addAction(source_action)

        # Set destination
        destination_action = QAction(
            QIcon('src/ui/destination.svg'), "Add destination", self)
        destination_action.triggered.connect(
            lambda: self.set_folder(self, "destination", "main"))
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
        self.delallRadio.clicked.connect(self.mark_all)

    # -----------------
    # ----- SLOTS -----
    # -----------------

    # ----- TOOLBAR -----

    # @Slot()
    @staticmethod  # Set source/destination
    def set_folder(self, folder, sender):
        folder_path = QFileDialog.getExistingDirectory(
            parent=self, caption=f"Select {folder}", dir=expanduser("~"))
        if folder_path:
            if folder == "source":
                self.source = folder_path
                self.sourceEdit.setText(folder_path)
            else:
                self.destination = folder_path
                self.destEdit.setText(folder_path)
            if sender == "main":
                write_log(f"{folder.capitalize()}: {folder_path}")

    @Slot()  # Configuration
    def config_action(self):
        dialog = ConfigDialog(self.config)
        dialog.config_updated.connect(self.config_updated)
        dialog.exec()

    @Slot()
    def config_updated(self):
        self.config = load_config()

        # Source/destination
        self.source = self.config['source']
        self.destination = self.config['destination']
        self.sourceEdit.setText(self.source)
        self.destEdit.setText(self.destination)
        write_log(f"Source: {self.source}\nDestination: {self.destination}")
        if self.config['options']:
            write_log(f"Additional options: "
                      f"{", ".join(self.config['options'])}")

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
        self.statusbar.showMessage("Listing deletions...")
        self.delList.clear()
        try:
            deletions = get_deletions(self.source, self.destination)
            if deletions:
                write_log(f"{len(deletions)} deletion(s) found.")
                self.delallRadio.setEnabled(True)
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
            write_log("Error while listing deletions.", e)
            self.statusbar.showMessage("Deletions could not be listed.")

    @Slot()
    def run_sync(self):

        # Delete files/folders
        entities = [path.join(self.destination,self.delList.item(index).text())
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
            result = sync(self.source, self.destination, self.config['options'])
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
            self.delallRadio.setChecked(False)
            self.delallRadio.setEnabled(False)
            self.syncButton.setEnabled(False)


class ConfigDialog(ConfigDlg, QDialog):
    config_updated = Signal(dict)
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Default source/destination
        self.sourceEdit.setText(config['source'])
        self.destEdit.setText(config['destination'])
        self.sourceButton.clicked.connect(
            lambda: MainWindow.set_folder(self, "source", "config"))
        self.destButton.clicked.connect(
            lambda: MainWindow.set_folder(self, "destination", "config"))

        # Additional options
        if config['options']:
            self.optionsEdit.setPlainText(", ".join(config['options']))

        self.buttonBox.accepted.connect(lambda: self.save(config))


    @Slot()
    def save(self, config):

        # Default source/destination
        config['source'] = self.sourceEdit.text()
        config['destination'] = self.destEdit.text()

        # Additional options
        config['options'] = list(set(
            self.optionsEdit.toPlainText().split(", "))) if (
            self.optionsEdit.toPlainText().strip()) else None
        if config['options']:
            if bool(set(config['options'])
                    & {"-av", "--archive", "-a", "--verbose", "-v"}):
                write_log("Warning: --archive (-a) and --verbose (-v) "
                          "are default options (-av)!")
                config['options'] = [option for option in config['options']
                                     if option not in ("-av", "--archive", "-a",
                                                       "--verbose", "-v")]
        try:
            save_config(config)
        except Exception as e:
            write_log("Error while saving configurations!", e)
        self.config_updated.emit(config)


class AboutDialog(AboutDlg, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.description.setText("arXive: a CLI/GUI frontend for "
                                 "<a href='https://rsync.samba.org/'>rsync</a>")
        self.version.setText("v0.0")
        url = "https://github.com/gaaldvd/arxive?tab=readme-ov-file#arXive"
        self.link.setText(f"<a href='{url}'>Visit GitHub page</a>")


# main function
def main():
    """Main function."""

    app = QApplication(sys.argv)
    window = MainWindow()

    # Create session log
    try:
        create_session_log()
    except Exception as e:
        write_log(f"Error while creating session log: {e}")
        window.statusbar.showMessage("Session log could not be created.")

    # Load config file
    try:
        window.config = load_config()
        write_log("Configurations loaded.")
    except Exception as e:
        write_log("Error while loading configurations!", e)
        window.statusbar.showMessage("Configurations could not be loaded.")

    # Determine source, destination and options
    window.source, window.destination = None, None
    if len(sys.argv) > 1:
        window.source, window.destination = sys.argv[1], sys.argv[2]
    else:
        window.source = window.config['source']
        window.destination = window.config['destination']
    if not path.exists(window.source):
        write_log(f"Warning! Invalid source: {window.source}")
        window.source = None
    else:
        window.sourceEdit.setText(window.source)
    if not path.exists(window.destination):
        write_log(f"Warning! Invalid destination: {window.destination}")
        window.destination = None
    else:
        window.destEdit.setText(window.destination)
        window.options = window.config['options']
    window.statusbar.showMessage("Ready.")
    write_log(f"Source: {window.source}\nDestination: {window.destination}")
    if window.options:
        write_log(f"Additional options: {", ".join(window.options)}")

    # Setting up UI...
    window.show()
    app.exec()


# script body
if __name__ == '__main__':
    main()
