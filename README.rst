Danube Cloud :: Image API Server 
################################

Shipment is a minimal and read-only `IMGAPI <https://images.joyent.com/docs/>`__ server application written in Python (Flask).


Development Guide
=================

It is expected that ``/opt/shipment`` directory exists, so once you clone the git repo, make sure it symlink's to /opt/shipment.

Installation
------------

All dependencies are stored in ``requirements.txt`` file. Install them in order to run the server::

        pip install -r doc/requirements.txt

Update PYTHONPATH, so Python can import from shipment directory::

        export PYTHONPATH="$PYTHONPATH:/opt/shipment"

By default, the server is looking into the root directory for datasets directory (eg. /datasets). However, you can override this by setting the system variable SHIPMENT_IMAGE_DIR to the path you prefer. If you would like to use some sample data, set it "/opt/shipment/doc/examples/datasets"::

        export SHIPMENT_IMAGE_DIR="/opt/shipment/doc/examples/datasets"


Run
---

Start development server::

        python bin/run.py


Links
=====

- Homepage: https://danubecloud.org
- Wiki: https://github.com/erigones/esdc-ce/wiki
- Bug Tracker: https://github.com/erigones/esdc-shipment/issues
- Twitter: https://twitter.com/danubecloud
- Mailing list: `danubecloud@googlegroups.com <danubecloud+subscribe@googlegroups.com>`__
- IRC: `irc.freenode.net#danubecloud <https://webchat.freenode.net/#danubecloud>`__


License
=======

::

    Copyright 2016 Erigones, s. r. o.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this project except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

