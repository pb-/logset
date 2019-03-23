import re
import os

STORE = os.getenv('LOGSET_STORE')
BUFFER_SIZE = 1 << 16
VALID_REPO = re.compile(r'^\w+$').match


def _dir(repo):
    if not STORE:
        raise ValueError('LOGSET_STORE is not set')

    return os.path.join(STORE, repo)


def get_offsets(repo):
    if not VALID_REPO(repo):
        return None

    directory = _dir(repo)

    if not os.path.exists(directory):
        return None

    return {
        name: os.stat(os.path.join(directory, name)).st_size
        for name in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, name))
    }


def get_slice(repo, name, offset, length):
    file_name = os.path.join(_dir(repo), name)

    with open(file_name, 'rb') as f:
        f.seek(offset)

        while length:
            data = f.read(min(length, BUFFER_SIZE))
            yield data
            length -= len(data)


def append_slice(repo, name, f, length):
    file_name = os.path.join(_dir(repo), name)

    with open(file_name, 'ab') as log:
        while length:
            data = f.read(min(length, BUFFER_SIZE))
            log.write(data)
            length -= len(data)
