import logging

import pandas as pd

GZIP_MAGIC = b'\x1f\x8b'


class MoveAppsPickle:
    """
    Reads the pickle an App produced.

    MoveApps dictates the file path and it carries no extension, so pandas cannot infer the
    compression from the file name. It is determined from the file content instead.

    Deliberately read-only: the cargo-agent never writes a pickle, it writes JSON statistics.
    """

    @staticmethod
    def read(path: str):
        """
        Reads a pickle, compressed or not.

        Apps built against a Python SDK before `v3` write uncompressed pickles, and such output still
        reaches the cargo-agent. Both flavours have to stay readable.

        :param path: path to the pickle to read
        :return: the unpickled data
        """
        compression = MoveAppsPickle.detect_compression(path=path)
        logging.info(f'reading pickle \'{path}\' (compression: {compression})')
        return pd.read_pickle(path, compression=compression)

    @staticmethod
    def detect_compression(path: str) -> str | None:
        """
        Determines the compression of a pickle from its first bytes instead of from its name.

        :param path: path to the pickle to inspect
        :return: `'gzip'` for a gzip-compressed file, otherwise `None`, which is how pandas is told
            not to decompress at all
        """
        with open(path, 'rb') as probe:
            return 'gzip' if probe.read(len(GZIP_MAGIC)) == GZIP_MAGIC else None
