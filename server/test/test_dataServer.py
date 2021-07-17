#!/venv/bin/python

# external dependencies
import unittest
import mock

# internal dependencies
from server.dataServer import runMediaGrab, serveMediaInfo, submitMediaInfoRecord


class Test_dataServer(unittest.TestCase):

    @mock.patch("os.getenv")
    @mock.patch("builtins.open", create=True)
    def test_serveMediaInfo(self, openMock, osGetEnvMock):

        #config fake data
        fakeFileContent = "fakeFileContent"
        class FakeFile:
            def read(self):
                return fakeFileContent

        # config mocks
        osGetEnvMock.return_value = "fake env return"
        openMock.return_value = FakeFile()

        content = serveMediaInfo()

        self.assertEqual(fakeFileContent, content)
        

    @mock.patch("server.interfaces.MediaIndexFileInterface.writeNewRecordToMediaInfoFile", create=True)
    def test_submitMediaInfoRecord(self, writeNewRecordToMediaInfoFileMock):

        #config fake data
        fakeData = {
            "mediaName": "fakeMediaName",
            "latestSeason": "1",
            "latestEpisode": "2",
            "blacklistTerms": "blacklistTerm1,blacklistTerm2 , blacklistTerm3  "
        }

        expectedMediaName = "fakeMediaName"
        expectedLatestSeason = 1
        expectedLatestEpisode = 2
        expectedBlacklistTerms = ["blacklistTerm1", "blacklistTerm2", "blacklistTerm3" ]

        # config mock
        writeNewRecordToMediaInfoFileMock = mock.MagicMock(return_value=True)
        
        result = submitMediaInfoRecord(fakeData)

        self.assertEqual(True, result)
        writeNewRecordToMediaInfoFileMock.assert_called_with(expectedMediaName, expectedLatestSeason, expectedLatestEpisode, expectedBlacklistTerms)


    @mock.patch("subprocess.check_call")
    @mock.patch("os.getenv")
    def test_runMediaGrab(self, osGetEnvMock, checkCallMock):

        # config fake data
        fakeOsGetEnvValue = "fakeOsGetEnvValue"

        # config mock
        osGetEnvMock.return_value = "fakeOsGetEnvValue"

        result = runMediaGrab()


        checkCallMock.assert_called_with(['venv/bin/python', 'Main.py'], cwd=fakeOsGetEnvValue)