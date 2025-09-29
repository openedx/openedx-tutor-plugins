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


Non-Tutor Install Instructions
******************************

If you wish to achieve the same setup without tutor you'll need to do the
following:

1. Install the `openedx-ltistore` python library in the edx-platform python
   environment.

.. code-block::

   pip install openedx-ltistore

2. Add the following settings to your edx-platform LMS/CMS Settings.

.. code-block::

   OPEN_EDX_FILTERS_CONFIG = {
       "org.openedx.xblock.lti_consumer.configuration.listed.v1": {
           "fail_silently": false,
           "pipeline": [
               "lti_store.pipelines.GetLtiConfigurations"
           ]
       }
   }

3. Enable the `lti_consumer.enable_external_config_filter` waffle flag. Run the followi

.. code-block::

   ./manage.py lms waffle_flag --create --everyone lti_consumer.enable_external_config_filter

4. Run migrations for the lti_stor app.

.. code-block::

   ./manage.py lms migrate lti_store


License
*******

This software is licensed under the terms of the AGPLv3.
