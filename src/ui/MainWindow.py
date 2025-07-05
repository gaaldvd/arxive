# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QPlainTextEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QStatusBar, QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 600)
        MainWindow.setMinimumSize(QSize(800, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.sessionCtrl = QWidget(self.centralwidget)
        self.sessionCtrl.setObjectName(u"sessionCtrl")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sessionCtrl.sizePolicy().hasHeightForWidth())
        self.sessionCtrl.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.sessionCtrl)
        self.gridLayout.setObjectName(u"gridLayout")
        self.sourceEdit = QLineEdit(self.sessionCtrl)
        self.sourceEdit.setObjectName(u"sourceEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sourceEdit.sizePolicy().hasHeightForWidth())
        self.sourceEdit.setSizePolicy(sizePolicy1)
        self.sourceEdit.setMinimumSize(QSize(300, 0))
        self.sourceEdit.setReadOnly(True)

        self.gridLayout.addWidget(self.sourceEdit, 0, 1, 1, 1)

        self.destLabel = QLabel(self.sessionCtrl)
        self.destLabel.setObjectName(u"destLabel")
        sizePolicy1.setHeightForWidth(self.destLabel.sizePolicy().hasHeightForWidth())
        self.destLabel.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.destLabel, 1, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.destEdit = QLineEdit(self.sessionCtrl)
        self.destEdit.setObjectName(u"destEdit")
        sizePolicy1.setHeightForWidth(self.destEdit.sizePolicy().hasHeightForWidth())
        self.destEdit.setSizePolicy(sizePolicy1)
        self.destEdit.setMinimumSize(QSize(300, 0))
        self.destEdit.setReadOnly(True)

        self.gridLayout.addWidget(self.destEdit, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.listdelButton = QPushButton(self.sessionCtrl)
        self.listdelButton.setObjectName(u"listdelButton")
        self.listdelButton.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.listdelButton.sizePolicy().hasHeightForWidth())
        self.listdelButton.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.listdelButton, 0, 4, 1, 1)

        self.syncButton = QPushButton(self.sessionCtrl)
        self.syncButton.setObjectName(u"syncButton")
        self.syncButton.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.syncButton.sizePolicy().hasHeightForWidth())
        self.syncButton.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.syncButton, 1, 4, 1, 1)

        self.sourceLabel = QLabel(self.sessionCtrl)
        self.sourceLabel.setObjectName(u"sourceLabel")
        sizePolicy1.setHeightForWidth(self.sourceLabel.sizePolicy().hasHeightForWidth())
        self.sourceLabel.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.sourceLabel, 0, 0, 1, 1)

        self.delallRadio = QRadioButton(self.sessionCtrl)
        self.delallRadio.setObjectName(u"delallRadio")
        self.delallRadio.setEnabled(False)

        self.gridLayout.addWidget(self.delallRadio, 1, 3, 1, 1)


        self.verticalLayout.addWidget(self.sessionCtrl)

        self.delList = QListWidget(self.centralwidget)
        self.delList.setObjectName(u"delList")

        self.verticalLayout.addWidget(self.delList)

        self.consoleOutput = QPlainTextEdit(self.centralwidget)
        self.consoleOutput.setObjectName(u"consoleOutput")
        self.consoleOutput.setReadOnly(True)

        self.verticalLayout.addWidget(self.consoleOutput)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolbar = QToolBar(MainWindow)
        self.toolbar.setObjectName(u"toolbar")
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(32, 32))
        self.toolbar.setFloatable(False)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"arXive", None))
        self.sourceEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Set source directory...", None))
        self.destLabel.setText(QCoreApplication.translate("MainWindow", u"Destination:", None))
        self.destEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Set destination directory...", None))
        self.listdelButton.setText(QCoreApplication.translate("MainWindow", u"List deletions", None))
        self.syncButton.setText(QCoreApplication.translate("MainWindow", u"Run sync", None))
        self.sourceLabel.setText(QCoreApplication.translate("MainWindow", u"Source:", None))
        self.delallRadio.setText(QCoreApplication.translate("MainWindow", u"Delete all", None))
        self.toolbar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolbar", None))
    # retranslateUi

