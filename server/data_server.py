#!/venv/bin/python

# external dependencies
import json
import os
from server.interfaces.MediaIndexFileInterface import removeRecordFromMediaInfoFile, updateRecordInMediaInfoFile, writeNewRecordToMediaInfoFile

# internal dependencies
from server.page_server import serveIndex
import subprocess

def serveMediaInfo():
    f = open(os.getenv("MEDIA_INDEX_FILE_LOCATION"), "r")
    mediaIndexFileContent = f.read()
    return mediaIndexFileContent


def submitMediaInfoRecord(data):

    # extract data
    mediaName = data['mediaName']
    latestSeason = int(data['latestSeason'])
    latestEpisode = int(data['latestEpisode'])
    blacklistTerms = data['blacklistTerms']

    blacklistTerms = [ term.replace(" ", "") for term in blacklistTerms.split(",") if len(term) > 0]

    return writeNewRecordToMediaInfoFile(mediaName, latestSeason, latestEpisode, blacklistTerms)


def deleteMediaInfoRecord(recordIndex):
    return removeRecordFromMediaInfoFile(recordIndex)


def updateMediaInfoRecord(newMediaIndexRecord, recordIndex):
    newMediaIndexRecord = json.loads(newMediaIndexRecord)

    return updateRecordInMediaInfoFile(newMediaIndexRecord, recordIndex)
    

def runMediaGrab():
    mediaGrabDir = os.getenv("MEDIA_GRAB_DIRECTORY")

    subprocess.check_call(['venv/bin/python', 'Main.py'], cwd=mediaGrabDir)

    return True