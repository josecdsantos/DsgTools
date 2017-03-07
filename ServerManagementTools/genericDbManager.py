# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-11-22
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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
#General imports
from osgeo import ogr
from uuid import uuid4
import codecs, os, json, binascii

#DSG Tools imports
from DsgTools.Factories.DbFactory.dbFactory import DbFactory 
from DsgTools.CustomWidgets.progressWidget import ProgressWidget
from DsgTools.Utils.utils import Utils
from DsgTools.dsgEnums import DsgEnums

#PyQt4 imports
from PyQt4.Qt import QObject

class GenericDbManager(QObject):
    """
    This class manages the permissions on dsgtools databases.
    """
    def __init__(self, serverAbstractDb, dbDict, edgvVersion, parentWidget = None):
        super(GenericDbManager,self).__init__()
        self.parentWidget = parentWidget
        self.dbDict = dbDict
        self.serverAbstractDb = serverAbstractDb
        self.adminDb = self.instantiateAdminDb(serverAbstractDb)
        self.utils = Utils()
        self.extensionDict = {'EarthCoverage':'.dsgearthcov', 
                    'Customization':'.dsgcustom', 
                    'Style':'.dsgstyle', 
                    'ValidationConfig':'.dsgvalidcfg', 
                    'FieldToolBoxConfig':'.reclas',
                    'Permission':'.dsgperm'}
        self.edgvVersion = edgvVersion

    def getManagerType(self):
        return str(self.__class__).split('.')[-1].replace('\'>', '').replace('Manager','')

    def instantiateAbstractDb(self, dbName):
        """
        Instantiates an abstractDb.
        """
        if dbName not in self.dbDict.keys():
            (host, port, user, password) = self.serverAbstractDb.getParamsFromConectedDb()
            abstractDb = DbFactory().createDbFactory('QPSQL')
            abstractDb.connectDatabaseWithParameters(host, port, dbName, user, password)
        else:
            abstractDb = self.dbDict[dbName]
        return abstractDb

    def instantiateAdminDb(self, serverAbstractDb):
        """
        Instantiates dsgtools_admindb in the same server as serverAbstractDb. 
        If dsgtools_admindb does not exists, instantiateAdminDb calls createAdminDb
        """
        (host, port, user, password) = serverAbstractDb.getParamsFromConectedDb()
        adminDb = DbFactory().createDbFactory('QPSQL')
        if not serverAbstractDb.hasAdminDb():
            return self.createAdminDb(serverAbstractDb, adminDb, host, port, user, password)
        adminDb.connectDatabaseWithParameters(host, port, 'dsgtools_admindb', user, password)
        return adminDb
            
    def instantiateTemplateDb(self, edgvVersion):
        """
        Instantiates a templateDb in the same server as serverAbstractDb. 
        If template does not exists, instantiateAdminDb calls createTemplate
        """
        templateName = self.serverAbstractDb.getTemplateName(edgvVersion)
        hasTemplate = self.serverAbstractDb.checkTemplate(edgvVersion)
        if not hasTemplate:
            self.serverAbstractDb.createTemplateDatabase(edgvVersion)
            templateDb = self.instantiateAbstractDb(templateName)
            templateDb.setStructureFromSql(edgvVersion, 4674)
            templateDb.setDbAsTemplate(version = edgvVersion)
        else:
            templateDb = self.instantiateAbstractDb(templateName)
        return templateDb

    def createAdminDb(self, serverAbstractDb, adminDb, host, port, user, password):
        """
        Creates dsgtools_admindb
        """
        serverAbstractDb.createAdminDb()
        adminDb.connectDatabaseWithParameters(host, port, 'dsgtools_admindb', user, password)
        sqlPath = adminDb.getCreationSqlPath('admin')
        adminDb.runSqlFromFile(sqlPath)
        return adminDb

    def getSettings(self):
        """
        Gets all profiles from public.permission_profile
        """
        settingType = self.getManagerType()
        return self.adminDb.getAllSettingsFromAdminDb(settingType)

    def getSetting(self, name, edgvVersion):
        """
        Get setting from corresponding table on dsgtools_admindb
        """
        settingType = self.getManagerType()
        settingDict = json.loads(self.adminDb.getSettingFromAdminDb(settingType, name, edgvVersion))
        if not settingDict:
            raise Exception(self.tr("Setting ")+ settingType +self.tr(" not found on dsgtools_admindb!"))
        return settingDict

    def createSetting(self, settingName, edgvVersion, jsonDict):
        """
        Creates setting on dsgtools_admindb.
        """
        settingType = self.getManagerType()
        if isinstance(jsonDict,dict):
            jsonDict = json.dumps(jsonDict,sort_keys=True, indent=4)
        self.adminDb.insertSettingIntoAdminDb(settingType, settingName, jsonDict, edgvVersion)

    def updateSetting(self, settingName, newJsonDict, edgvVersion = None):
        """
        Generic update. Can be reimplenented in child methods.
        1. Get property dict from adminDb 
        """
        if not edgvVersion:
            edgvVersion = self.edgvVersion
        errorDict = dict()
        successList = []
        settingType = self.getManagerType()
        propertyDict = self.adminDb.getPropertyPerspectiveDict(settingType, DsgEnums.Property, versionFilter = edgvVersion)
        if settingName in propertyDict.keys():
            rollbackList = []
            self.adminDb.db.transaction()
            try:
                for dbName in propertyDict[settingName]:
                    abstractDb = self.instantiateAbstractDb(dbName)
                    abstractDb.db.transaction()
                    rollbackList.append(abstractDb)
                    abstractDb.updateRecordFromPropertyTable(settingType, settingName, edgvVersion, newJsonDict)
                self.adminDb.updateRecordFromPropertyTable(settingType, settingName, edgvVersion, newJsonDict)
                for abstractDb in rollbackList:
                    abstractDb.db.commit()
                self.adminDb.db.commit()
                successList = [i for i in propertyDict[settingName]]
            except Exception as e:
                for abstractDb in rollbackList:
                    abstractDb.db.rollback()
                self.adminDb.db.rollback()
                errorDict[dbName] = str(e.args[0])
        return (successList, errorDict)

    def importSetting(self, fullFilePath):
        """
        Function to import profile into dsgtools_admindb. It has the following steps:
        1. Reads inputJsonFilePath and parses it into a python dict;
        2. Validates inputPermissionDict;
        3. Tries to insert into database, if there is an error, abstractDb raises an error which is also raised by importProfile
        """
        #getting profile name
        settingName = os.path.basename(fullFilePath).split('.')[0]
        #getting json
        inputJsonDict, inputJson = self.utils.readJsonFile(fullFilePath, returnFileAndDict = True)
        #error handling and json validation
        if inputJsonDict == dict():
            raise Exception(self.tr("Not valid DsgTools property file!"))
        if not self.validateJsonSetting(inputJsonDict):
            raise Exception(self.tr("Not valid DsgTools property file!"))
        if 'version' in inputJsonDict.keys():
            edgvVersion = inputJsonDict['version']
        else:
            edgvVersion = inputJsonDict.keys()[0].split('_')[-1]
        try:
            self.createSetting(settingName, edgvVersion, inputJson)
        except Exception as e:
            raise Exception(self.tr("Error importing setting ") + settingName +': '+e.args[0])

    def batchImportSettings(self, profilesDir):
        """
        1. Get all properties in profilesDir;
        2. Import each using importSetting;
        """
        importList = []
        for profile in os.walk(profilesDir).next()[2]:
            if self.extensionDict[self.getManagerType()] in os.path.basename(profile):
                importList.append(os.path.join(profilesDir,profile))
        for profileFile in importList:
            self.importSetting(profileFile)

    def exportSetting(self, profileName, edgvVersion, outputPath):
        """
        1. Get setting from dsgtools_admindb;
        2. Export it to outputPath.
        """
        jsonDict = self.getSetting(profileName, edgvVersion)
        outputFile = os.path.join(outputPath, profileName+self.extensionDict[self.getManagerType()])
        with open(outputFile, 'w') as outfile:
            json.dump(jsonDict, outfile, sort_keys=True, indent=4)
    
    def batchExportSettings(self, outputDir):
        """
        1. Get all settings from corresponding table in dsgtools_admindb;
        2. Export each using exportSetting.
        """
        settingDict = self.getSettings()
        for edgvVersion in settingDict.keys():
            outputPath = os.path.join(outputDir,edgvVersion)
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)
            for profileName in settingDict[edgvVersion]:
                self.exportSetting(profileName, edgvVersion, outputPath)

    def getPropertyPerspectiveDict(self, viewType = DsgEnums.Property):
        """
        Gets a dict in the format:
        if viewType == 'customization': {customizationName: ['-list of databases with customization']}
        if viewType == 'database': {databaseName: ['-list of customizations with customization']}
        """
        settingType = self.getManagerType()
        return self.adminDb.getPropertyPerspectiveDict(settingType, viewType)
    
    def getSettingVersion(self, settingName):
        settingType = self.getManagerType()
        return self.adminDb.getSettingVersion(settingType, settingName)
    
    def validateJsonSetting(self, inputJsonDict):
        """
        reimplemented in each child
        """
        return True
    
    def getRecordFromAdminDb(self, propertyName, edgvVersion):
        settingType = self.getManagerType()
        return self.adminDb.getRecordFromAdminDb(settingType, propertyName, edgvVersion)

    def createAndInstall(self, configName, newJsonDict, edgvVersion, dbList = []):
        self.createSetting(configName, edgvVersion, newJsonDict)
        self.installSetting(configName,dbNameList = dbList)

    def installSetting(self, configName, dbNameList = []):
        """
        Generic install. Can be reimplenented in child methods.
        """
        errorDict = dict()
        settingType = self.getManagerType()
        if dbNameList == []:
            dbNameList = self.dbDict.keys()
        successList = []
        configEdgvVersion = self.getSettingVersion(configName)
        for dbName in dbNameList:
            abstractDb = self.instantiateAbstractDb(dbName)
            edgvVersion = abstractDb.getDatabaseVersion()
            if edgvVersion != configEdgvVersion:
                errorDict[dbName] = self.tr('Database version missmatch.')
                continue
            recDict = self.adminDb.getRecordFromAdminDb(settingType, configName, edgvVersion)
            try:
                if not abstractDb.checkIfExistsConfigTable(settingType):
                    abstractDb.createPropertyTable(settingType)
            except Exception as e:
                errorDict[dbName] = str(e.args[0])
                continue
            try:
                abstractDb.db.transaction()
                self.adminDb.db.transaction()
                abstractDb.insertRecordInsidePropertyTable(settingType, recDict, edgvVersion)
                dbOid = abstractDb.getDbOID()
                self.adminDb.insertInstalledRecordIntoAdminDb(settingType, recDict, dbOid)
                abstractDb.db.commit()
                self.adminDb.db.commit()
            except Exception as e:
                abstractDb.db.rollback()
                self.adminDb.db.rollback()
                errorDict[dbName] = str(e.args[0])
            successList.append(dbName)
        return (successList, errorDict)
    
    def deleteSetting(self, configName, dbNameList = []):
        """
        Generic remove. Can be reimplenented in child methods.
        1. Get property dict from adminDb 
        """
        errorDict = dict()
        successList = []
        settingType = self.getManagerType()
        propertyDict = self.adminDb.getPropertyPerspectiveDict(settingType, DsgEnums.Property)
        if configName in propertyDict.keys():
            for dbName in propertyDict[configName]:
                abstractDb = self.instantiateAbstractDb(dbName)
                edgvVersion = abstractDb.getDatabaseVersion()
                try:
                    abstractDb.db.transaction()
                    self.adminDb.db.transaction()
                    abstractDb.removeRecordFromPropertyTable(settingType, configName, edgvVersion)
                    self.adminDb.removeRecordFromPropertyTable(settingType, configName, edgvVersion)
                    abstractDb.db.commit()
                    self.adminDb.db.commit()
                except Exception as e:
                    abstractDb.db.rollback()
                    self.adminDb.db.rollback()
                    errorDict[dbName] = str(e.args[0])
                successList.append(dbName)
        return (successList, errorDict)

    def uninstallSetting(self, configName, dbNameList = []):
        """
        Generic uninstall. Can be reimplenented in child methods.
        This can uninstall setting on a list of databases or in all databases (if dbNameList == [])
        """
        errorDict = dict()
        successList = []
        settingType = self.getManagerType()
        propertyDict = self.adminDb.getPropertyPerspectiveDict(settingType, DsgEnums.Property)
        if configName in propertyDict.keys():
            if dbNameList == []: #builds filter dbList to uninstall in all installed databases
                dbList = propertyDict[configName]
            else: #builds filter dbList to uninstall in databases in dbNameList
                dbList = [i for i in propertyDict[configName] if i in dbNameList]
            for dbName in dbList:
                abstractDb = self.instantiateAbstractDb(dbName)
                edgvVersion = abstractDb.getDatabaseVersion()
                try:
                    abstractDb.db.transaction()
                    self.adminDb.db.transaction()
                    abstractDb.removeRecordFromPropertyTable(settingType, configName, edgvVersion)
                    self.adminDb.uninstallPropertyOnAdminDb(settingType, configName, edgvVersion, dbName = dbName)
                    abstractDb.db.commit()
                    self.adminDb.db.commit()
                except Exception as e:
                    abstractDb.db.rollback()
                    self.adminDb.db.rollback()
                    errorDict[dbName] = str(e.args[0])
                successList.append(dbName)
        return (successList, errorDict)