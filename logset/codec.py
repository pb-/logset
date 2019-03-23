import re
from operator import ne
from itertools import takewhile, repeat
from functools import partial

OFFSET = re.compile(r'^(?P<name>\w+) (?P<offset>\d+)\n$')
SLICE_INFO = re.compile(r'^(?P<name>\w+) (?P<offset>\d+) (?P<length>\d+)\n$')


def encode_offsets(offsets):
    return ''.join(
        f'{name} {offset}\n' for name, offset in offsets.items()
    ).encode('ascii') + b'\n'


def decode_offset(line):
    m = OFFSET.match(line.decode('ascii'))
    return (m.group('name'), int(m.group('offset')))


def read_offsets(f):
    return dict(map(
        decode_offset,
        takewhile(
            partial(ne, b'\n'),
            (f.readline() for _ in repeat(None)))))


def encode_slice_info(name, offset, length):
    return f'{name} {offset} {length}\n'.encode('ascii')


def decode_slice_info(line):
    m = SLICE_INFO.match(line.decode('ascii'))
    return {
        'name': m.group('name'),
        'offset': int(m.group('offset')),
        'length': int(m.group('length')),
    }


def read_slice_info(f):
    line = f.readline()
    if not line:
        return None

    return decode_slice_info(line)
