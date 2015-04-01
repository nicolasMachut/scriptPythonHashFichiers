#!/usr/bin/python
__author__ = 'nicolas'
import os
import hashlib
import pymongo
import sys

connection = pymongo.Connection()
db = connection["HASHTP"]
hashs = db["hashs"]

# fichier d'exclusion
fichier = open("exclusion.conf", "r")
excludedFolders = fichier.readlines()
print("%s Fichiers exclu du check" %len(excludedFolders))

for folder in excludedFolders:
    print(folder.rstrip('\n\r'))

fichier.close()


path = "/home/nicolas/testPython"
print("\n")

def fileToSha1(filePath):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(filePath, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()

args = sys.argv
if len(args) > 1 and args[1] == "check":
    db.hashs.remove()
    for path, dirs, files in os.walk(path):
        for filename in files:
            filePath = path + "/" + filename
            fileSha1 = fileToSha1(filePath)
            hashs.insert({"path": filePath, "hash": fileSha1})
else:
    path = "/home/nicolas/testPython"
    countModifiedFiles = 0
    countAddedFiles = 0
    for path, dirs, files in os.walk(path):
        for filename in files:
            filePath = path + "/" + filename
            fileSha1 = fileToSha1(filePath)
            result = db.hashs.find({"path": filePath})

            if result.count() == 0:
                print("%s à été ajouté" %filePath)
                countAddedFiles += 1
            else:
                hashFoundInBdd = result[0]["hash"]
                if hashFoundInBdd != fileSha1:
                    countModifiedFiles += 1
                    print("%s à été modifié" %filePath)

    print("\n")
    print("%s fichier(s) modfié(s)" %countModifiedFiles)
    print("%s fichier(s) ajouté(s)" %countAddedFiles)