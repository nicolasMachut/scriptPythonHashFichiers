import hashlib
import parameters
import xml.etree.ElementTree as ET
import os

def getExcludedDirectories():
    # get excluded directories from config.xml
    excludedDirectories = []
    tree = ET.parse(parameters.CONFIG_FILE)
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
    parameters.logFile.write(message + "\n")
    print(message)

def getDeletedFiles ():
    deletedFiles = 0
    allFilesInServer = []
    for path, dirs, files in os.walk(parameters.SERVER_PATH):
        for filename in files:
            allFilesInServer.append((filename))

    fileInDatabase = parameters.db.hashs.find({})

    for oneFileInDB in fileInDatabase:
        chemin = str(oneFileInDB["path"])
        print(chemin)
        exist = False
        for oneFileInHardDrive in allFilesInServer:
            splitedFilePath = chemin.split("/")
            fileName = splitedFilePath[len(splitedFilePath) -1]
            if(oneFileInHardDrive == fileName):
                exist = True
                break

        if(exist == False):
            log(chemin + " à été supprimé")
            deletedFiles += 1

    log(str(deletedFiles) + " fichier(s) supprimé(s)")