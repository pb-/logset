from flask import Flask, abort, request, Response

from . import codec, store

app = Flask(__name__)


@app.route('/<repo>/offsets', methods=['GET'])
def get_offsets(repo):
    offsets = store.get_offsets(repo)
    if offsets is None:
        abort(404)

    return Response(
        codec.encode_offsets(store.get_offsets(repo)),
        mimetype='application/octet-stream'
    )


@app.route('/<repo>/pull', methods=['POST'])
def post_pull(repo):
    local_offsets = store.get_offsets(repo)
    if local_offsets is None:
        abort(404)

    remote_offsets = codec.read_offsets(request.stream)

    def generate():
        yield codec.encode_offsets(local_offsets)
        for name, local_offset in local_offsets.items():
            remote_offset = remote_offsets.get(name, 0)

            if remote_offset < local_offset:
                length = local_offset - remote_offset
                yield codec.encode_slice_info(name, remote_offset, length)
                yield from store.get_slice(repo, name, remote_offset, length)

    return Response(generate(), mimetype='application/octet-stream')


@app.route('/<repo>/push', methods=['POST'])
def post_push(repo):
    local_offsets = store.get_offsets(repo)
    if local_offsets is None:
        abort(404)

    while True:
        slice_info = codec.read_slice_info(request.stream)
        if not slice_info:
            return '', 201

        if local_offsets.get(slice_info['name'], 0) != slice_info['offset']:
            abort(403)

        store.append_slice(
            repo, slice_info['name'], request.stream, slice_info['length'])
