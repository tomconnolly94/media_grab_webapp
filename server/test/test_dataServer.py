#!/venv/bin/python

# external dependencies
import unittest
import mock

# internal dependencies
from server.dataServer import serveMediaInfo

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