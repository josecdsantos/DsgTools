# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cria_moldura_dialog_base.ui'
#
# Created: Thu Nov 06 19:18:45 2014
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_CriaMoldura(object):
    def setupUi(self, CriaMoldura):
        CriaMoldura.setObjectName(_fromUtf8("CriaMoldura"))
        CriaMoldura.resize(500, 350)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CriaMoldura.sizePolicy().hasHeightForWidth())
        CriaMoldura.setSizePolicy(sizePolicy)
        CriaMoldura.setMinimumSize(QtCore.QSize(500, 350))
        CriaMoldura.setMaximumSize(QtCore.QSize(500, 350))
        self.horizontalLayoutWidget = QtGui.QWidget(CriaMoldura)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 440, 51))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.arquivoCriaMolduraLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.arquivoCriaMolduraLineEdit.setObjectName(_fromUtf8("arquivoCriaMolduraLineEdit"))
        self.horizontalLayout.addWidget(self.arquivoCriaMolduraLineEdit)
        spacerItem1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonBuscarArquivoCriaMoldura = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonBuscarArquivoCriaMoldura.setObjectName(_fromUtf8("pushButtonBuscarArquivoCriaMoldura"))
        self.horizontalLayout.addWidget(self.pushButtonBuscarArquivoCriaMoldura)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(CriaMoldura)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(30, 90, 440, 41))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.coordSysCriaMolduraLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.coordSysCriaMolduraLineEdit.setObjectName(_fromUtf8("coordSysCriaMolduraLineEdit"))
        self.horizontalLayout_2.addWidget(self.coordSysCriaMolduraLineEdit)
        spacerItem3 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.horizontalLayoutWidget_4 = QtGui.QWidget(CriaMoldura)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(30, 310, 441, 31))
        self.horizontalLayoutWidget_4.setObjectName(_fromUtf8("horizontalLayoutWidget_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.pushButtonOkCriaMoldura = QtGui.QPushButton(self.horizontalLayoutWidget_4)
        self.pushButtonOkCriaMoldura.setObjectName(_fromUtf8("pushButtonOkCriaMoldura"))
        self.horizontalLayout_4.addWidget(self.pushButtonOkCriaMoldura)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.pushButtonCancelarCriaMoldura = QtGui.QPushButton(self.horizontalLayoutWidget_4)
        self.pushButtonCancelarCriaMoldura.setObjectName(_fromUtf8("pushButtonCancelarCriaMoldura"))
        self.horizontalLayout_4.addWidget(self.pushButtonCancelarCriaMoldura)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.horizontalLayoutWidget_3 = QtGui.QWidget(CriaMoldura)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(30, 150, 441, 41))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(self.horizontalLayoutWidget_3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.comboBoxEscala = QtGui.QComboBox(self.horizontalLayoutWidget_3)
        self.comboBoxEscala.setObjectName(_fromUtf8("comboBoxEscala"))
        self.horizontalLayout_3.addWidget(self.comboBoxEscala)
        self.horizontalLayoutWidget_5 = QtGui.QWidget(CriaMoldura)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(30, 200, 441, 41))
        self.horizontalLayoutWidget_5.setObjectName(_fromUtf8("horizontalLayoutWidget_5"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_5.setMargin(0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.radioButtonMI = QtGui.QRadioButton(self.horizontalLayoutWidget_5)
        self.radioButtonMI.setObjectName(_fromUtf8("radioButtonMI"))
        self.horizontalLayout_5.addWidget(self.radioButtonMI)
        self.comboBoxMI = QtGui.QComboBox(self.horizontalLayoutWidget_5)
        self.comboBoxMI.setEnabled(False)
        self.comboBoxMI.setObjectName(_fromUtf8("comboBoxMI"))
        self.horizontalLayout_5.addWidget(self.comboBoxMI)
        self.horizontalLayoutWidget_6 = QtGui.QWidget(CriaMoldura)
        self.horizontalLayoutWidget_6.setGeometry(QtCore.QRect(30, 250, 441, 41))
        self.horizontalLayoutWidget_6.setObjectName(_fromUtf8("horizontalLayoutWidget_6"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout_6.setMargin(0)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.radioButtonINOM = QtGui.QRadioButton(self.horizontalLayoutWidget_6)
        self.radioButtonINOM.setObjectName(_fromUtf8("radioButtonINOM"))
        self.horizontalLayout_6.addWidget(self.radioButtonINOM)
        self.comboBoxINOM = QtGui.QComboBox(self.horizontalLayoutWidget_6)
        self.comboBoxINOM.setEnabled(False)
        self.comboBoxINOM.setObjectName(_fromUtf8("comboBoxINOM"))
        self.horizontalLayout_6.addWidget(self.comboBoxINOM)

        self.retranslateUi(CriaMoldura)
        QtCore.QObject.connect(self.pushButtonCancelarCriaMoldura, QtCore.SIGNAL(_fromUtf8("clicked()")), CriaMoldura.close)
        QtCore.QMetaObject.connectSlotsByName(CriaMoldura)

    def retranslateUi(self, CriaMoldura):
        CriaMoldura.setWindowTitle(_translate("CriaMoldura", "Create Frame", None))
        self.label.setText(_translate("CriaMoldura", "File   ", None))
        self.pushButtonBuscarArquivoCriaMoldura.setText(_translate("CriaMoldura", "Search", None))
        self.label_2.setText(_translate("CriaMoldura", "Coordinate System", None))
        self.pushButtonOkCriaMoldura.setText(_translate("CriaMoldura", "Ok", None))
        self.pushButtonCancelarCriaMoldura.setText(_translate("CriaMoldura", "Cancel", None))
        self.label_3.setText(_translate("CriaMoldura", "Scale", None))
        self.radioButtonMI.setText(_translate("CriaMoldura", "MI", None))
        self.radioButtonINOM.setText(_translate("CriaMoldura", "INOM", None))

