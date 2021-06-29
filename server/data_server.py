#!/venv/bin/python

# external dependencies
import json
import os
from server.interfaces.MediaIndexFileInterface import removeRecordFromMediaInfoFile, updateRecordInMediaInfoFile, writeNewRecordToMediaInfoFile

# internal dependencies
from server.page_server import serveIndex


def serveMediaInfo():
    f = open(os.getenv("MEDIA_INDEX_FILE_LOCATION"), "r")
    mediaIndexFileContent = f.read()
    return mediaIndexFileContent


def submitMediaInfoRecord(form):

    # extract data
    mediaName = form.get('mediaName')
    latestSeason = int(form.get('latestSeason'))
    latestEpisode = int(form.get('latestEpisode'))
    blacklistTerms = form.get('blacklistTerms')

    blacklistTerms = [ term.replace(" ", "") for term in blacklistTerms.split(",") ]

    writeNewRecordToMediaInfoFile(mediaName, latestSeason, latestEpisode, blacklistTerms)


def deleteMediaInfoRecord(recordName):
    removeRecordFromMediaInfoFile(recordName)


def updateMediaInfoRecord(newMediaIndexRecord):
    newMediaIndexRecord = json.loads(newMediaIndexRecord)
    print(newMediaIndexRecord)

    return updateRecordInMediaInfoFile(newMediaIndexRecord)
    