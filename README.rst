===========
rtsp-to-hls
===========

RTSP to HLS streaming

* Free software: MIT license

Dependencies
------------

FFmpeg
~~~~~~
* https://linuxize.com/post/how-to-install-ffmpeg-on-ubuntu-18-04/


Install PyPI requirments
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ pip install -r requirements.txt


Usage
-----

.. code:: bash

    $ python main.py --sources 'rtsp://192.168.0.101:554/cam/realmonitor?channel=1&subtype=0' --names camera

Then go to http://127.0.0.1:5001
