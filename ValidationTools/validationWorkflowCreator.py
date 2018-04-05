# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-04
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba@dsg.eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os
from os.path import expanduser

from qgis.core import QgsMessageLog

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, Qt, QSettings
from PyQt4.QtGui import QListWidgetItem, QMessageBox, QMenu, QApplication, QCursor, QFileDialog
from PyQt4.QtSql import QSqlDatabase,QSqlQuery



FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'validationWorkflowCreator.ui'))

class ValidationWorkflowCreator(QtGui.QDialog, FORM_CLASS):
    def __init__(self, validationManager, parameterDict = None, parent = None):
        """Constructor."""
        super(ValidationWorkflowCreator, self).__init__(parent)
        self.validationManager = validationManager
        self.setupUi(self)
        self.workflowOrderedWidget.parent = self

    @pyqtSlot(bool)
    def on_okPushButton_clicked(self):
        """
        1. Validate widget
        2. Export jsonDict
        """
        if not self.validate():
            msg = self.invalidatedReason()
            QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Errors on interface! Check log for details!'))
            return
        self.done(1)
    
    @pyqtSlot(bool)
    def on_cancelPushButton_clicked(self):
        self.close()
    
    def validate(self, parameterDict):
        if 'orderedAttributeRulesWidget' not in parameterDict.keys():
            return False
        return True
    
    def invalidatedReason(self):
        return self.tr('Invalid tag for attributeRulesEditor!')
    
    def getParameterDict(self):
        return {'orderedAttributeRulesWidget':self.attributeRulesWidget.getParameterDict()}
    
    def populateInterface(self, parameterDict):
        self.attributeRulesWidget.populateInterface(parameterDict['orderedAttributeRulesWidget'])
    
    def validateJson(self, parameterDict):
        if ['orderedAttributeRulesWidget'] != parameterDict.keys():
            return False
        return self.attributeRulesWidget.validateJson(parameterDict['orderedAttributeRulesWidget'])
