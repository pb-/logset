import sys

import requests

from . import codec


def get(session, url):
    r = session.get(url, stream=True)
    r.raise_for_status()
    return r


def post(session, url, data):
    r = session.post(url, data=data, stream=True)
    r.raise_for_status()
    return r


def offsets(session, url):
    return codec.read_offsets(get(session, f"{url}/offsets").raw)


def pull(session, url, local_offsets):
    return post(
        session, f"{url}/pull", codec.encode_offsets(local_offsets)).raw


def push(session, url, f):
    return post(session, f"{url}/push", f)


def has_data(source_offsets, dest_offsets):
    return any(
        dest_offsets.get(name, 0) < offset
        for name, offset in source_offsets.items())


def sync_step(session, source_url, dest_url, dest_offsets):
    source = pull(session, source_url, dest_offsets)
    source_offsets = codec.read_offsets(source)

    with_data = has_data(source_offsets, dest_offsets)
    if with_data:
        push(session, dest_url, source)

    return source_offsets, with_data


def sync(local_url, remote_url):
    session = requests.Session()

    local_offsets = offsets(session, local_url)
    remote_offsets, with_data = sync_step(
        session, remote_url, local_url, local_offsets)

    if remote_offsets != local_offsets:
        sync_step(session, local_url, remote_url, remote_offsets)

    session.close()

    return with_data


def run():
    sync(*sys.argv[1:])
