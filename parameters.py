import datetime
import pymongo

# constants fields
CONFIG_FILE = "/home/nicolas/Dropbox/Workspace/hashProject/config.xml"
SERVER_PATH = "/home/nicolas/testPython"
LOG_FILE = "/var/www/html/HashTp/logs/" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# opened logFile, Used to log
logFile = None

# mongodb database connection
connection = pymongo.Connection()
db = connection["HASHTP"]
hashs = db["hashs"]