# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-11-24
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Brazilian Army - Geographic Service Bureau
        email                : suporte.dsgtools@dsg.eb.mil.br
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

# Qt imports
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.Qt import QObject

# QGIS imports
from qgis.core import QgsVectorLayer,QgsDataSourceURI, QgsMessageLog
from qgis.utils import iface

#DsgTools imports
from DsgTools.Factories.DbFactory.abstractDb import AbstractDb

class EDGVLayer(QObject):
    qmlLoaded = pyqtSignal()
    
    def __init__(self, abstractDb, codeList):
        """Constructor."""
        super(EDGVLayer, self).__init__()
        
        self.abstractDb = abstractDb
        self.codeList = codeList
        self.uri = QgsDataSourceURI()

        self.qmlLoaded.connect(self.codeList.setState)        
        
    def load(self, crs, idSubgrupo = None):
        vlayerQml = os.path.join(self.abstractDb.getQmlDir(), self.qmlName+'.qml')
        
        host = self.abstractDb.db.hostName()
        port = self.abstractDb.db.port()
        database = self.abstractDb.db.databaseName()
        user = self.abstractDb.db.userName()
        password = self.abstractDb.db.password()

        vlayer = iface.addVectorLayer(self.uri.uri(), self.layer_name, self.provider)
        if not vlayer:
            return None

        vlayer.setCrs(crs)
        vlayer.loadNamedStyle(vlayerQml, False)
        attrList = vlayer.attributeList()
        for i in attrList:
            if vlayer.editorWidgetV2(i) == 'ValueRelation':
                groupList = iface.legendInterface().groups()
                groupRelationshipList = iface.legendInterface().groupLayerRelationship()
                if database not in groupList:
                    idx = iface.legendInterface().addGroup(database, True,-1)
                    domainIdGroup = iface.legendInterface().addGroup(self.tr("Dominios"), True, idx)
                else:
                    idx = groupList.index(database)
                    if "Dominios" not in groupList[idx::]:
                        domainIdGroup = iface.legendInterface().addGroup(self.tr("Dominios"), True, idx)
                    else:
                        domainIdGroup = groupList[idx::].index("Dominios")

                valueRelationDict = vlayer.editorWidgetV2Config(i)
                domainTableName = valueRelationDict['Layer']
                loadedLayers = iface.legendInterface().layers()
                domainLoaded = False
                for ll in loadedLayers:
                    if ll.name() == domainTableName:
                        candidateUri = QgsDataSourceURI(ll.dataProvider().dataSourceUri())
                        if host == candidateUri.host() and database == candidateUri.database() and port == int(candidateUri.port()):
                            domainLoaded = True
                            domLayer = ll
                if not domainLoaded:
                    uri = "dbname='%s' host=%s port=%s user='%s' password='%s' key=code table=\"dominios\".\"%s\" sql=" % (database, host, port, user, password, domainTableName)
                    #TODO Load domain layer into a group
                    domLayer = iface.addVectorLayer(uri, domainTableName, self.provider)
                    iface.legendInterface().moveLayer(domLayer, domainIdGroup)
                valueRelationDict['Layer'] = domLayer.id()
                vlayer.setEditorWidgetV2Config(i,valueRelationDict)

        self.qmlLoaded.emit()
        

        iface.legendInterface().moveLayer(vlayer, idSubgrupo)
            
        if not vlayer.isValid():
            QgsMessageLog.logMessage(vlayer.error().summary(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)

        return vlayer

    def loadDomainTable(self,name):
        pass