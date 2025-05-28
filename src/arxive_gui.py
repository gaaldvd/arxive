# arXive GUI script

from sys import argv, exit as close
from arxive_common import *

from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QIcon
from ui.MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)

        # Spacer for widgets
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                             QtWidgets.QSizePolicy.Expanding)

        # ----- TOOLBAR -----

        # CONFIG
        config_action = QAction(
            QIcon('src/ui/configure.svg'), "Configuration", self)
        config_action.triggered.connect(self.config_action)
        self.toolbar.addAction(config_action)

        # <--- left side
        self.toolbar.addWidget(spacer)
        # right side --->

        # ABOUT
        about_action = QAction(QIcon('src/ui/help-about.svg'), "About", self)
        about_action.triggered.connect(self.about_action)
        self.toolbar.addAction(about_action)

        # EXIT
        exit_action = QAction(QIcon('src/ui/window-close.svg'), "Exit", self)
        exit_action.triggered.connect(self.exit_action)
        self.toolbar.addAction(exit_action)

        # -------------------

        self.runButton.clicked.connect(self.run_sync)

    # -----------------
    # ----- SLOTS -----
    # -----------------

    # ----- TOOLBAR -----

    @Slot()  # config
    def config_action(self): print("Configuration...")

    @Slot()   # about
    def about_action(self): print("About...")

    @Slot()  # exit
    def exit_action(self): close("Goodbye!")

    # -------------------

    @Slot()
    def run_sync(self): print("Run sync...")


# main function
def main():
    """Main function."""

    app = QtWidgets.QApplication(argv)
    window = MainWindow()

    # Create session log, load config file
    create_session_log()
    config = load_config()
    if config is False:
        # TODO show alert
        close("Error, see session log for details!")

    # Determine source and destination from CLI arguments
    source, destination = None, None
    if len(argv) > 1:
        if not path.exists(argv[1]) or not path.exists(argv[2]):
            # TODO alert about invalid source/destination
            pass
        else:
            source, destination = argv[1], argv[2]
            window.sourceEdit.setText(source)
            window.destEdit.setText(destination)
            window.statusbar.showMessage("Ready.")

    print(f"Source: {source}\nDestination: {destination}")

    # Setting up UI...
    window.show()
    app.exec()


# script body
if __name__ == '__main__':
    main()
