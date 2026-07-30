import os
import tempfile
from unittest import TestCase

from src.moveapps_pickle import MoveAppsPickle
from test.config.definitions import ROOT_DIR
from test.config.fixtures import gzip_copy


class TestMoveAppsPickle(TestCase):
    """
    MoveApps hands the cargo-agent a path without a file extension, so none of these cases may rely
    on the file name to tell compressed from uncompressed data.
    """

    def setUp(self) -> None:
        self.sut = MoveAppsPickle()
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_it_should_detect_an_uncompressed_pickle(self):
        # prepare
        legacy = self.__fixture('input4_LatLon.pickle')

        # execute
        actual = self.sut.detect_compression(path=legacy)

        # verify: `None` is how pandas is told not to decompress at all
        self.assertIsNone(actual)

    def test_it_should_detect_a_gzip_compressed_pickle(self):
        # prepare
        compressed = gzip_copy(self.__fixture('input4_LatLon.pickle'), self.__tmp_file('output_file'))

        # execute
        actual = self.sut.detect_compression(path=compressed)

        # verify
        self.assertEqual('gzip', actual)

    def test_it_should_read_an_uncompressed_pickle(self):
        # prepare
        legacy = self.__fixture('input4_LatLon.pickle')

        # execute
        actual = self.sut.read(path=legacy)

        # verify
        self.assertEqual(3, len(actual.trajectories))

    def test_it_should_read_a_gzip_compressed_pickle_named_without_an_extension(self):
        # prepare
        compressed = gzip_copy(self.__fixture('input4_LatLon.pickle'), self.__tmp_file('output_file'))

        # execute
        actual = self.sut.read(path=compressed)

        # verify
        self.assertEqual(3, len(actual.trajectories))

    def __fixture(self, file_name: str) -> str:
        return os.path.join(ROOT_DIR, 'test', 'resources', 'moving_pandas_trajectory_collection', file_name)

    def __tmp_file(self, file_name: str) -> str:
        return os.path.join(self.tmp.name, file_name)
