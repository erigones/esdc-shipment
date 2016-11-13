from os import path
from functools import wraps

from flask import abort

from shipment.app import IMAGE_DIR, IMAGE_MANIFEST_NAME, IMAGE_FILE_NAME
from shipment.utils import validate_uuid


def valid_image_or_404(check_manifest=False, check_file=False):
    """Check if uuid is valid or return 404"""
    def decorator(view):
        @wraps(view)
        def wrap(uuid):
            try:
                uuid = validate_uuid(uuid)
            except ValueError:
                return abort(404)

            args = []

            if check_manifest:
                image_manifest_path = path.join(IMAGE_DIR, uuid, IMAGE_MANIFEST_NAME)
                if not path.exists(image_manifest_path):
                    return abort(404)
                args.append(image_manifest_path)

            if check_file:
                image_file_path = path.join(IMAGE_DIR, uuid, IMAGE_FILE_NAME)
                if not path.exists(image_file_path):
                    return abort(404)
                args.append(image_file_path)

            return view(uuid, *args)
        return wrap
    return decorator
