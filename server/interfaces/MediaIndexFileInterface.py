#!/venv/bin/python

# external dependencies
import os
import json

# internal dependencies


writeFile = True
    

def loadMediaFile():
	"""
	loadMediaFile opens the MediaIndex.json file and loads the content into a list of MediaInfoRecord objects
	:testedWith: None IO/glue code which does not require testing
	:return: a list of MediaInfoRecord's loaded from the MediaIndex.json
	"""
	mediaIndexFileLocation = os.getenv("MEDIA_INDEX_FILE_LOCATION")
	#logging.info(f"MediaIndex File: {mediaIndexFileLocation}")

	with open(mediaIndexFileLocation, "r") as mediaIndexfile:
		return json.loads(mediaIndexfile.read())["media"]


def writeNewRecordToMediaIndexFile(name, latestSeason, latestEpisode, blacklistTerms):

    mediaIndexRecords = loadMediaFile()

    for record in mediaIndexRecords:
        if name == record["name"]:
            return None


    newRecord = {
        "name": name, 
        "typeSpecificData": {
            "latestSeason": latestSeason, 
            "latestEpisode": latestEpisode
        }, 
        "blacklistTerms": blacklistTerms
    }

    mediaIndexRecords.append(newRecord)
    media = { "media": mediaIndexRecords }
    
    if writeFile:
        with open(os.getenv("MEDIA_INDEX_FILE_LOCATION"), "w") as mediaFileTarget:
            json.dump(media, mediaFileTarget)
