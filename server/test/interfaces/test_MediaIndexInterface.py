#!/venv/bin/python

# external dependencies
import json
import unittest
import mock

# internal dependencies
from server.interfaces.MediaIndexFileInterface import loadMediaFile
from server.test.testUtilities import FakeFile


class Test_MediaIndexFileInterface(unittest.TestCase):

    @mock.patch("builtins.open", create=True)
    @mock.patch("os.getenv")
    def test_loadMediaFile(self, osGetEnvMock, openMock):

        #config fake data
        fakeMediaItems = [
            {
                "mediaName": "fakeMediaName",
                "latestSeason": "1",
                "latestEpisode": "2",
                "blacklistTerms": "blacklistTerm1,blacklistTerm2 , blacklistTerm3  "
            },
            {
                "mediaName": "fakeMediaName",
                "latestSeason": "1",
                "latestEpisode": "2",
                "blacklistTerms": "blacklistTerm1,blacklistTerm2 , blacklistTerm3  "
            }
        ]
        fakeFileContentDict = {
            "media": fakeMediaItems
        }
        fakeFileContent = json.dumps(fakeFileContentDict)
        fakeEnvReturn = "fakeEnvReturn"

        # config mocks
        osGetEnvMock.return_value = fakeEnvReturn
        openMock.return_value = FakeFile(fakeFileContent)

        content = loadMediaFile()

        self.assertEqual(fakeMediaItems, content)
        openMock.assert_called_with(fakeEnvReturn, "r")
        
