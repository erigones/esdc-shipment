"""
Simple implementation of IMGAPI.

https://github.com/joyent/sdc-imgapi/blob/master/docs/index.md
"""
from flask import make_response, send_file

from shipment import __version__, __description__, __copyright__
from shipment.app import app, NGINX_ENABLED
from shipment.utils import json_response, load_manifest, list_manifests, get_image_file_md5, get_image_file_size
from shipment.decorators import valid_image_or_404


@app.route('/')
def index():
    """Index info page.
    """
    return json_response({
        'shipment': __description__,
        'version': __version__,
        'copyright': __copyright__,
    })


@app.route('/images', methods=('GET',))
def list_images():
    """ListImages (GET /images)

    Return all images (array of json objects).
    """
    return json_response(list_manifests())


# noinspection PyUnusedLocal
@app.route('/images/<uuid>', methods=('GET',))
@valid_image_or_404(check_manifest=True)
def get_image(uuid, image_manifest_path):
    """GetImage (GET /images/:uuid)

    Return image manifest (json object).
    """
    return json_response(load_manifest(image_manifest_path))


# noinspection PyUnusedLocal
@app.route('/images/<uuid>/file', methods=('GET',))
@valid_image_or_404(check_file=True)
def get_image_file(uuid, image_file_path):
    """GetImageFile (GET /images/:uuid/file)

    Return the image file.
    """
    encoded_md5 = get_image_file_md5(uuid, image_file_path)

    if NGINX_ENABLED:
        res = make_response('')
        res.headers['Content-Type'] = 'application/octet-stream'
        res.headers['X-Accel-Redirect'] = '/static/images/%s/file?md5=%s' % (uuid, encoded_md5)
    else:
        res = make_response(send_file(image_file_path, add_etags=False, cache_timeout=0))

    res.headers['Content-Length'] = get_image_file_size(image_file_path)
    res.headers['Content-MD5'] = encoded_md5

    return res


@app.route('/ping', methods=('GET',))
def ping():
    """Ping (GET /ping)

    A simple ping to check health of the image server.
    """
    return json_response({
        'ping': 'pong',
        'version': __version__,
        'imgapi': False,
    })


# noinspection PyUnusedLocal
@app.errorhandler(404)
def page_not_found(error):
    """404 handler.
    """
    return json_response({
        'code': 'ResourceNotFound',
        'message': 'Resource not found',
    }, status_code=404)
