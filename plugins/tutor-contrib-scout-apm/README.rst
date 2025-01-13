Scout APM plugin for `Tutor <https://docs.tutor.overhang.io>`_
==============================================================

This plugin allows Open edX LMS and Studio site operators add support for Scout APM monitoring.

Installation
------------

This will install the `Scout APM <https://scoutapm.com/>`_ plugin directly from Github::

    pip install git+https://github.com/openedx/openedx-tutor-plugins.git#subdirectory=plugins/tutor-contrib-scout-apm

Alternatively, you can clone the parent repository locally and install it from the checkout::

    git clone https://github.com/openedx/openedx-tutor-plugins.git
    cd openedx-tutor-plugins/plugins/tutor-contrib-scout-apm
    pip install -e .

Usage
-----

Once installed, run the following commands to enable it::

    tutor plugins enable scout-apm
    tutor images build openedx-dev

Add the following entries to your Tutor ``config.yml`` file:

* ``SCOUT_KEY``: Get this from your Scout APM account.
* ``SCOUT_NAME``: A user friendly name for your application. It will have "| LMS" or "| Studio" appended to it. So if you put "Sumac Test Server", the two Scout apps being reported will be "Sumac Test Server | LMS" and "Sumac Test Server | Studio".

License
-------

This software is licensed under the terms of the AGPLv3.
