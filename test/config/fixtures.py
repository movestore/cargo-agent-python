import gzip
import shutil


def gzip_copy(source: str, target: str) -> str:
    """
    Writes a gzip-compressed copy of `source` to `target`.

    Lets a test simulate the output of an App on Python SDK v3 without adding a second set of binary
    fixtures to the repository. The pickle payload itself is copied byte for byte.

    :param source: path to the uncompressed file
    :param target: path to write the compressed copy to
    :return: `target`, for convenience
    """
    with open(source, 'rb') as plain, gzip.open(target, 'wb') as compressed:
        shutil.copyfileobj(plain, compressed)
    return target
