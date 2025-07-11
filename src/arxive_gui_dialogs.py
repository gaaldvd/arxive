# arXive GUI dialogs

from arxive_gui import set_dir
from arxive_common import validate_options

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Signal, Slot

from ui.Config import Ui_Dialog as ConfigDlg
from ui.About import Ui_Dialog as AboutDlg


class ConfigDialog(ConfigDlg, QDialog):
    config_updated = Signal(dict)
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Default source/destination
        self.sourceEdit.setText(config.source)
        self.destEdit.setText(config.destination)
        self.sourceButton.clicked.connect(
            lambda: set_dir(self, "source"))
        self.destButton.clicked.connect(
            lambda: set_dir(self, "destination"))

        # Additional options
        if config.options:
            self.optionsEdit.setPlainText(", ".join(config.options))

        self.buttonBox.accepted.connect(lambda: self.save(config))


    @Slot()
    def save(self, config):

        # Default source/destination
        config.source = self.sourceEdit.text()
        config.destination = self.destEdit.text()

        # Additional options
        config.options = list(set(
            self.optionsEdit.toPlainText().split(", "))) if (
            self.optionsEdit.toPlainText().strip()) else None
        if config.options:
            config.options = validate_options(config.options)

        try:
            config.save()
            print("Configurations saved.")
        except Exception as e:
            print(f"Error while saving configurations: {e}")
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