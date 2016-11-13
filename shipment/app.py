import os
import sys

from flask import Flask


# Initialize app
app = Flask('shipment')
app.config.update({'DEBUG': False, 'TESTING': False, 'PROPAGATE_EXCEPTIONS': True})
app.config.from_envvar('SHIPMENT_SETTINGS', silent=True)

IMAGE_DIR = app.config.get('IMAGE_DIR', os.environ.get('SHIPMENT_IMAGE_DIR', None))
NGINX_ENABLED = app.config.get('NGINX_ENABLED', os.environ.get('SHIPMENT_NGINX_ENABLED', False))

if not IMAGE_DIR:
    IMAGE_DIR = '/datasets'

IMAGE_DIR = os.path.abspath(IMAGE_DIR)
IMAGE_MANIFEST_NAME = 'manifest'
IMAGE_FILE_NAME = 'file'
IMAGE_FILE_MD5_NAME = 'file.md5'

sys.stdout.write('Using "%s" as IMAGE_DIR...\n' % IMAGE_DIR)

if not os.access(IMAGE_DIR, os.R_OK | os.W_OK | os.X_OK):
    sys.stderr.write('IMAGE_DIR "%s" does not exist or is not accessible. Exiting...\n' % IMAGE_DIR)
    sys.exit(1)

# Register views
# noinspection PyUnresolvedReferences
from shipment import views
