ltistore plugin for `Tutor <https://docs.tutor.edly.io>`__
##########################################################

A plugin to install and enable the openedx-ltistore for reausable lti configurations.


Installation
************

.. code-block:: bash

    pip install git+https://github.com/openedx/openedx-tutor-plugins.git#subdirectory=plugins/tutor-contrib-ltistore

For development:

.. code-block:: bash

    cd openedx-tutor-plugins/plugins/tutor-contrib-ltistore
    pip install -e '.[dev]'

Usage
*****

.. code-block:: bash

    tutor plugins enable ltistore
    tutor images build openedx
    tutor local do init --limit=ltistore
    tutor local launch --skip-build --non-interactive

For development:

.. code-block:: bash

    tutor plugins enable ltistore
    tutor images build openedx-dev
    tutor dev do init --limit=ltistore
    tutor dev launch --skip-build --non-interactive

License
*******

This software is licensed under the terms of the AGPLv3.
