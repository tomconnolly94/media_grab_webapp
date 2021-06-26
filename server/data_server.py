#!/venv/bin/python

# external dependencies
import os
from server.interfaces.MediaIndexFileInterface import writeNewRecordToMediaIndexFile

# internal dependencies
from server.page_server import serveIndex


def serveMediaIndex():
    f = open(os.getenv("MEDIA_INDEX_FILE_LOCATION"), "r")
    mediaIndexFileContent = f.read()
    return mediaIndexFileContent

def submitMediaIndexRecord(request):

    # extract data
    mediaName = request.form.get('mediaName')
    latestSeason = int(request.form.get('latestSeason'))
    latestEpisode = int(request.form.get('latestEpisode'))
    blacklistTerms = request.form.get('blacklistTerms')

    blacklistTerms = [ term.replace(" ", "") for term in blacklistTerms.split(",") ]

    writeNewRecordToMediaIndexFile(mediaName, latestSeason, latestEpisode, blacklistTerms)


    return serveIndex()

