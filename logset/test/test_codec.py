from io import BytesIO

from .. import codec


def test_offsets():
    offsets = {
        'abc': 1,
        'def': 49859,
    }

    io = BytesIO(codec.encode_offsets(offsets))
    assert codec.read_offsets(io) == offsets


def test_slice_info():
    slice_info = {
        'name': 'xyz',
        'offset': 10,
        'length': 200,
    }

    io = BytesIO(codec.encode_slice_info(**slice_info))
    assert codec.read_slice_info(io) == slice_info
