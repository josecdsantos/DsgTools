# -*- coding: utf-8 -*-
"""
/***************************************************************************
MinimumAreaTool
                                 A QGIS plugin
Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2016-08-02
        git sha              : $Format:%H$
        copyright            : (C) 2016 by  Jossan Costa - Surveying Technician @ Brazilian Army
                                            Felipe Diniz - Cartographic Engineer @ Brazilian Army
        email                : jossan.costa@eb.mil.br
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
import json

# Qt imports
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.QtWidgets import QMessageBox, QAction
from qgis.PyQt.QtGui import QIcon, QColor
from qgis.PyQt.QtCore import QSettings, pyqtSignal, pyqtSlot, QObject
from qgis.PyQt.Qt import QWidget, QObject

#qgis imports
import qgis.utils
from qgis.gui import QgsMessageBar
from qgis.core import Qgis
#DsgTools Imports
from .shapeTool import ShapeTool
from .customSizeSetter import CustomSizeSetter

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'minimumAreaTool.ui'))

class MinimumAreaTool(QWidget,FORM_CLASS):
    PROJECT_STATE_VAR = "minimumAreaToolState"

    def __init__(self, iface, parent=None):
        """
        Constructor
        """
        super(MinimumAreaTool, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.splitter.hide()
        self.iface = iface
        self.setScaleString('1:100000')
        self.scale = None
        self.shape = None
        self.size = None
        self.populateSizesComboBox()
        icon_path = ':/plugins/DsgTools/icons/minAreaTool.png'
        text = self.tr('DSGTools: Minimum Area Tool')
        self.showAction = self.add_action(icon_path, text, self.showPushButton.toggle, parent = self.parent)
        self.iface.registerMainWindowAction(self.showAction, '')
        icon_path = ':/plugins/DsgTools/icons/areaTool.png'
        text = self.tr('DSGTools: Draw Shape')
        self.shapeAction = self.add_action(icon_path, text, self.drawShape.click, parent = self.parent)
        self.iface.registerMainWindowAction(self.shapeAction, '')

    def add_action(self, icon_path, text, callback, parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        if parent:
            parent.addAction(action)
        return action
    
    def initGui(self):
        """
        Adds the tool bar in QGIS
        """
        self.iface.addToolBarWidget(self.splitter)
        
    def createDict(self, customDict = None):
        """
        Creates the dictionary used to create the geometry templates
        """
        self.sizes = {}
        self.sizes[u"25mm²"] = {'value': 25, 'shape': 'area'}
        self.sizes[u"4mm²"] = {'value': 4, 'shape': 'area'}
        self.sizes[u"1x1mm²"] = {'value': 1, 'shape': 'area'}
        self.sizes[u"0.8x0.8mm²"] = {'value': 0.64, 'shape': 'area'}
        self.sizes[u"0.8mm"] = {'value': 0.8,'shape': 'distance'}
        if customDict:
            for key in customDict:
                self.sizes[key] = customDict[key]
        
    def shapeComboSetter(self):
        """
        Sets the correct index for the shapes combo box according to the text select in the sizes combo box
        """
        if self.sizesComboBox.currentText() in list(self.sizes.keys()):
            if self.sizes[self.sizesComboBox.currentText()]['shape'] == 'distance':
                #In this case we should force the use of circle, due to the measurement shape = distance and set the shape combo box enabled(False)
                self.shapesComboBox.setCurrentIndex(2)
                self.shapesComboBox.setEnabled(False)
            else:
                self.shapesComboBox.setEnabled(True)
        else:
            self.shapesComboBox.setEnabled(True)

    def scaleString(self):
        """
        Reads the scale string from GUI.
        :return: (str) scale string.
        """
        return self.mScaleWidget.scaleString()

    def setScaleString(self, scale):
        """
        Sets a scale string to GUI.
        :param scale: (str) scale string.
        """
        self.mScaleWidget.setScaleString(scale)

    def color(self):
        """
        Reads color to be used on the generated geometry from the GUI.
        :return: (QColor) tuple of RGBA values for the color.
        """
        return self.mColorButton.color()

    def setColor(self, color):
        """
        Sets color to be used on the generated geometry to the GUI.
        :param color: (QColor) color to be set.
        """
        self.mColorButton.setColor(color)

    @pyqtSlot(int)
    def on_sizesComboBox_currentIndexChanged(self):
        """
        Slot used to check if the user selected 0.8mm (this is used for linear features).
        In this case we should force the use of circle and set the shape combo box enabled(False)
        """
        if self.sizesComboBox.currentIndex() != 0:
            self.shapeComboSetter()
    
    @pyqtSlot(int)
    def on_shapesComboBox_currentIndexChanged(self):
        """
        Slot used to check if the user selected 0.8mm (this is used for linear features).
        In this case we should force the use of circle and set the shape combo box enabled(False)
        """
        if self.shapesComboBox.currentIndex() != 0:
            self.shapeComboSetter()
    
    @pyqtSlot(bool)
    def on_drawShape_clicked(self):
        """
        Draws the select template shape on the map canvas
        """
        scaleText = self.scaleString()
        scale = int(scaleText.split(':')[-1].replace('.','').replace(',',''))/1000
        size = self.sizesComboBox.currentText()
        shape = self.shapesComboBox.currentText()
        validated = self.validateCombos(self.sizesComboBox.currentIndex(), self.shapesComboBox.currentIndex())
        if validated:
            crs = self.iface.mapCanvas().mapSettings().destinationCrs()
            if crs.mapUnits() == 2:
                self.iface.messageBar().pushMessage(self.tr('Critical!'), self.tr('This tool does not work with angular unit reference system!'), level=Qgis.Warning, duration=3)
            else:
                self.run(scale, size, shape)
        else:
            QMessageBox.warning(self.iface.mainWindow(), self.tr(u"Error!"), self.tr(u"<font color=red>Shape value not defined :</font><br><font color=blue>Define all values to activate tool!</font>"), QMessageBox.Close)              
    
    def run(self, scale, size, shape):
        """
        Runs the ShapeTool and set it as the current map tool
        """
        #checking the selected type
        if (self.sizes[size]['shape'] == 'area'):
            param = (float(scale)**2)*float(self.sizes[size]['value'])
        else:
            param = float(scale)*float(self.sizes[size]['value'])
        color = self.mColorButton.color()
        color.setAlpha(63)
        tool = ShapeTool(self.iface.mapCanvas(), shape, param, self.sizes[size]['shape'], color )
        tool.toolFinished.connect(self.refreshCombo)
        self.iface.mapCanvas().setMapTool(tool)

    def refreshCombo(self):
        """
        Re-enables the shapes combo
        """
        self.shapesComboBox.setEnabled(True)
    
    def validateCombos(self,size,shape):
        """
        Checks if all combos correctly selected
        """
        if size != 0 and shape != 0:
            return True
        else:
            return False

    def isToggled(self):
        """
        Identifies whether tool bar is toggled ("open").
        :return: (bool) if tool bar is toggled.
        """
        return self.showPushButton.isChecked()

    def setToggled(self, checked):
        """
        Set tool bar's toggling status (if it's "open").
        :param checked: (bool) if tool bar is toggled.
        """
        return self.showPushButton.setChecked(checked)

    @pyqtSlot(bool, name = 'on_showPushButton_toggled')
    def toggleBar(self, toggled=None):
        """
        Slot to show/hide the tool bar
        """
        if toggled is None:
            toggled = self.showPushButton.isChecked()
        if toggled:
            self.splitter.show()
        else:
            self.splitter.hide()
    
    def getCustomSizesDict(self):
        #get custom sizes from qsettings
        settings = QSettings()
        settings.beginGroup('DSGTools/CustomSizes/')
        currentSettings = settings.childGroups()
        settings.endGroup()
        customSizesDict = dict()
        #get each parameter
        for settingName in currentSettings:
            customSizesDict[settingName] = dict()
            settings = QSettings()
            settings.beginGroup('DSGTools/CustomSizes/'+settingName)
            customSizesDict[settingName]['shape'] = settings.value('shape')
            customSizesDict[settingName]['value'] = settings.value('value')
            settings.endGroup()
        return customSizesDict
    
    def addValueToCustomSizesDict(self, newValueDict):
        settings = QSettings()
        if not settings.contains('DSGTools/CustomSizes/'+newValueDict['comboText']+'/shape'):
            settings.beginGroup('DSGTools/CustomSizes/'+newValueDict['comboText'])
            settings.setValue('shape', newValueDict['shape'])
            settings.setValue('value', newValueDict['value'])
            settings.endGroup()
        self.populateSizesComboBox()
    
    def populateSizesComboBox(self):
        self.sizesComboBox.clear()
        self.sizesComboBox.addItem(self.tr('SIZES'))
        self.sizesComboBox.addItem(u'25mm²')
        self.sizesComboBox.addItem(u'4mm²')
        self.sizesComboBox.addItem(u'0.8x0.8mm²')
        self.sizesComboBox.addItem(u'1x1mm²')
        self.sizesComboBox.addItem(u'0.8mm')
        customSizesDict = self.getCustomSizesDict()
        self.createDict(customDict = customSizesDict)
        self.populateComboWithCustomSizes(customSizesDict)
    
    def updateAndPopulateSizes(self, sizeDict):
        self.size = sizeDict
        self.populateSizeComboBoxWithDict()
    
    def populateSizeComboBoxWithDict(self):
        self.sizesComboBox.clear()
        self.sizesComboBox.addItem(self.tr('SIZES'))
        for key in self.sizes:
            self.sizesComboBox.addItem(key)
    
    def populateComboWithCustomSizes(self, customSizesDict):
        """
        Add to sizesComboBox values from customSizesDict and adds values to self.sizes 
        """
        for size in list(customSizesDict.keys()):
            #add item to comboBox
            self.sizesComboBox.addItem(size)

    @pyqtSlot(bool)
    def on_createCustomSizesPushButton_clicked(self):
        """
        Opens custom size setter
        """
        customSizesDict = self.getCustomSizesDict()
        dlg = CustomSizeSetter(customSizesDict)
        dlg.sizeCreated.connect(self.addValueToCustomSizesDict)
        dlg.exec_()

    def state(self):
        """
        Reads current tool's attributes that compose its state.
        :return: (dict) an attribute value map that represents current tool's
                state.
        """
        return {
            "scale": self.scaleString(),
            "size": self.sizesComboBox.currentIndex(),
            "shape": self.shapesComboBox.currentIndex(),
            "color": self.color().getRgb(),
            "isOpen": self.isToggled()
        }

    def stateAsString(self, state=None):
        """
        Stringfied states is a simple and effective form of serializing objects for
        QGIS environment variable settings, as well as outside QGIS systems
        communications. This method transforms a tool's state map into a string.
        :param state: (dict) the map to be stringfied.
        :return: (str) stringfied tool state map.
        """
        state = state or self.state()
        return json.dumps(state)

    def stateFromString(self, state):
        """
        Reverts a string into a valid tool state map.
        :param state: (str) the map to be de-stringfied.
        :return: (dict) an attribute value map that represents current tool's
                state.
        """
        return json.loads(state)

    def validateState(self, state):
        """
        Verifies if a map is is a valid representation of a tool's state.
        :param state: (dict) the map to be checked.
        :return: (bool) whether the provided map represents a tool state.
        """
        return True

    def setState(self, state):
        """
        Updates tool's attributes related to its state.
        :param state: (dict) an attribute value map that represents current tool's
                    state.
        :return: (bool) whether given parameters reflects tool's state after
                aplying it.
        """
        if not self.validateState(state):
            return False
        self.setScaleString(state["scale"])
        self.sizesComboBox.setCurrentIndex(int(state["size"])),
        self.shapesComboBox.setCurrentIndex(int(state["shape"])),
        self.setColor(QColor(*state["color"]))
        self.setToggled(state["isOpen"])
        return True

    def unload(self):
        try:
            self.iface.unregisterMainWindowAction(self.showAction)
        except:
            pass
        try:
            self.iface.unregisterMainWindowAction(self.shapeAction)
        except:
            pass
