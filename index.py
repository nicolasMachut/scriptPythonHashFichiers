#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'nicolas'

# imports
import os
import hashlib
import pymongo
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

# constants fields
CONFIG_FILE = "/home/nicolas/Dropbox/Workspace/hashProject/config.xml"
SERVER_PATH = "/home/nicolas/testPython"
LOG_FILE = "hashTP.log"

# mongodb database connection
connection = pymongo.Connection()
db = connection["HASHTP"]
hashs = db["hashs"]


# open log file
logFile = open(LOG_FILE, "w")



def getExcludedDirectories():
    # get excluded directories from config.xml
    log("Charging configuration file")
    excludedDirectories = []
    tree = ET.parse(CONFIG_FILE)
    root = tree.getroot()
    print("Directories to exclude : ")
    for directory in root.iter('directory'):
        excludedDirectories.append(directory.text)

    print(excludedDirectories)
    return excludedDirectories

def fileToSha1(filePath):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(filePath, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()

def log(message):
    logFile.write(message + "\n")
    print(message)

def getDeletedFiles ():
    deletedFiles = 0
    allFilesInServer = []
    for path, dirs, files in os.walk(SERVER_PATH):
        for filename in files:
            allFilesInServer.append((filename))

    fileInDatabase = db.hashs.find({})

    for oneFileInDB in fileInDatabase:
        exist = False
        for oneFileInHardDrive in allFilesInServer:
            splitedFilePath = oneFileInDB["path"].split("/")
            fileName = splitedFilePath[len(splitedFilePath) -1]
            if(oneFileInHardDrive == fileName):
               exist = True
               break

        if(exist == False):
            log('File deleted : ' + oneFileInHardDrive)
            deletedFiles += 1

    print(str(deletedFiles) + " fichier(s) supprimé(s)")



excludedDirectories = getExcludedDirectories()
getDeletedFiles()


args = sys.argv
if len(args) > 1 and args[1] == "check":
    db.hashs.remove()
    path = SERVER_PATH
    for path, dirs, files in os.walk(path):
        for filename in files:
            filePath = path + "/" + filename
            fileSha1 = fileToSha1(filePath)
            hashs.insert({"path": filePath, "hash": fileSha1})
else:
    path = SERVER_PATH
    countModifiedFiles = 0
    countAddedFiles = 0
    for path, dirs, files in os.walk(path):
        for filename in files:
            filePath = path + "/" + filename
            fileSha1 = fileToSha1(filePath)
            result = db.hashs.find({"path": filePath})

            if result.count() == 0:
                log("%s à été ajouté" %filePath)
                countAddedFiles += 1
            else:
                hashFoundInBdd = result[0]["hash"]
                if hashFoundInBdd != fileSha1:
                    countModifiedFiles += 1
                    log("%s à été modifié" %filePath)

    log("%s fichier(s) modfié(s)" %countModifiedFiles)
    log("%s fichier(s) ajouté(s)" %countAddedFiles)


# close log file
logFile.close()