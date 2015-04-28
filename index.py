#!/usr/bin/python
__author__ = 'nicolas'

# imports
import os
import hashlib
import pymongo
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

# constants fields
CONFIG_FILE = "config.xml"
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
    print("Charging configuration file")

    tree = ET.parse(CONFIG_FILE)
    root = tree.getroot()
    for neighbor in root.iter('directory'):
        print(neighbor.attrib)

    # doc = minidom.parse(CONFIG_FILE)
    # if doc.hasChildNodes():
    #     for element in doc.getElementsByTagName('directory'):
    #         print(element.value())
    #
    # file = open(CONFIG_FILE, "r")
    # lines = file.readlines()
    # print("%s Fichiers exclu du check" % len(lines))
    # excludedDirectories = []
    # for folder in lines:
    #     excludedDirectories.append(folder.rstrip('\n\r'))
    #     print(folder.rstrip('\n\r'))
    # file.close()
    # return excludedDirectories

def fileToSha1(filePath):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(filePath, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()

def log (message):
    logFile.write(message + "\n")
    print(message)


excludedDirectories = getExcludedDirectories()

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