import sys
from re import compile
from os import path
from glob import iglob
from base64 import b64encode
from hashlib import md5
from collections import OrderedDict

from flask import json, make_response

from shipment.app import IMAGE_DIR, IMAGE_MANIFEST_NAME, IMAGE_FILE_MD5_NAME


RE_UUID = compile(r'[a-z0-9]{8}-([a-z0-9]{4}-){3}[a-z0-9]{12}')


def validate_uuid(uuid):
    """UUID input validator"""
    if not RE_UUID.search(uuid):
        raise ValueError('Invalid uuid')

    return uuid


def json_response(data, status_code=200):
    """Helper for returning json response"""
    if isinstance(data, (dict, tuple, list)):
        data = json.dumps(data, indent=4, separators=(',', ': '))

    res = make_response(data, status_code)
    res.headers['Content-Type'] = 'application/json'

    return res


def load_manifest(image_manifest_path):
    """Return contents of image manifest file (dict)"""
    with open(image_manifest_path, 'r') as fp:
        return json.loads(fp.read(), object_pairs_hook=OrderedDict)


def list_manifests():
    """Return list of contents of image manifest files (array of dicts)"""
    manifests = []

    for i in iglob(path.join(IMAGE_DIR, '*', IMAGE_MANIFEST_NAME)):
        # noinspection PyBroadException
        try:
            manifests.append(load_manifest(i))
        except Exception as ex:
            sys.stderr.write('Error (%s) reading file: %s\n' % (ex, i))
            continue

    return manifests


def _md5sum(fp, blocksize=65536):
    """Return base64 encoded md5 digest of large file object"""
    hasher = md5()
    buf = fp.read(blocksize)

    while len(buf) > 0:
        hasher.update(buf)
        buf = fp.read(blocksize)

    return b64encode(hasher.digest())


def get_image_file_md5(uuid, image_file_path):
    """Return image file's md5sum from cache or calculate and save it"""
    md5_cache = path.join(IMAGE_DIR, uuid, IMAGE_FILE_MD5_NAME)

    if path.exists(md5_cache):
        with open(md5_cache, 'r') as fp:
            enc_md5 = fp.read()
    else:
        with open(image_file_path, 'rb') as img_fp:
            enc_md5 = _md5sum(img_fp)
        with open(md5_cache, 'w') as fp:
            fp.write(enc_md5)

    return enc_md5


def get_image_file_size(image_file_path):
    """Return image file's size """
    return path.getsize(image_file_path)
