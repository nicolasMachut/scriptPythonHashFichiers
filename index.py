#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'nicolas'

# imports
import functions
import parameters
import sys
import os

# open log file
parameters.logFile = open(parameters.LOG_FILE, "w")

excludedDirectories = functions.getExcludedDirectories()

args = sys.argv
functions.log("Action : "+args[1])
if len(args) > 1 and args[1] == "analyse":
    parameters.db.hashs.remove()
    path = parameters.SERVER_PATH
    for path, dirs, files in os.walk(path):
        for filename in files:
            if path not in excludedDirectories:
                filePath = path + "/" + filename
                fileSha1 = functions.fileToSha1(filePath)
                functions.log("filePath :"+filePath+", Hash : "+fileSha1)
                parameters.hashs.insert({"path": filePath, "hash": fileSha1})

else:
    path = parameters.SERVER_PATH
    countModifiedFiles = 0
    countAddedFiles = 0
    for path, dirs, files in os.walk(path):
        for filename in files:
            if path not in excludedDirectories:
                filePath = path + "/" + filename
                fileSha1 = functions.fileToSha1(filePath)
                result = parameters.db.hashs.find({"path": filePath})

            if result.count() == 0:
                functions.log("%s à été ajouté" %filePath)
                countAddedFiles += 1
            else:
                hashFoundInBdd = result[0]["hash"]
                if hashFoundInBdd != fileSha1:
                    countModifiedFiles += 1
                    functions.log("%s à été modifié" %filePath)
    functions.getDeletedFiles()
    functions.log("%s fichier(s) modfié(s)" %countModifiedFiles)
    functions.log("%s fichier(s) ajouté(s)" %countAddedFiles)

parameters.logFile.close()