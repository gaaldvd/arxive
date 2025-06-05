# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QLabel, QLineEdit, QPlainTextEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(420, 300)
        Dialog.setMinimumSize(QSize(420, 300))
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.source = QLabel(Dialog)
        self.source.setObjectName(u"source")

        self.gridLayout.addWidget(self.source, 0, 0, 1, 1)

        self.sourceEdit = QLineEdit(Dialog)
        self.sourceEdit.setObjectName(u"sourceEdit")

        self.gridLayout.addWidget(self.sourceEdit, 0, 1, 1, 1)

        self.sourceButton = QPushButton(Dialog)
        self.sourceButton.setObjectName(u"sourceButton")

        self.gridLayout.addWidget(self.sourceButton, 0, 2, 1, 1)

        self.destination = QLabel(Dialog)
        self.destination.setObjectName(u"destination")

        self.gridLayout.addWidget(self.destination, 1, 0, 1, 1)

        self.destEdit = QLineEdit(Dialog)
        self.destEdit.setObjectName(u"destEdit")

        self.gridLayout.addWidget(self.destEdit, 1, 1, 1, 1)

        self.destButton = QPushButton(Dialog)
        self.destButton.setObjectName(u"destButton")

        self.gridLayout.addWidget(self.destButton, 1, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.options = QLabel(Dialog)
        self.options.setObjectName(u"options")

        self.verticalLayout.addWidget(self.options)

        self.optionsEdit = QPlainTextEdit(Dialog)
        self.optionsEdit.setObjectName(u"optionsEdit")

        self.verticalLayout.addWidget(self.optionsEdit)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)

        self.verticalLayout.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Configuration", None))
        self.source.setText(QCoreApplication.translate("Dialog", u"Default source:", None))
        self.sourceButton.setText(QCoreApplication.translate("Dialog", u"Select", None))
        self.destination.setText(QCoreApplication.translate("Dialog", u"Default destination:", None))
        self.destButton.setText(QCoreApplication.translate("Dialog", u"Select", None))
        self.options.setText(QCoreApplication.translate("Dialog", u"Additional options:", None))
    # retranslateUi

