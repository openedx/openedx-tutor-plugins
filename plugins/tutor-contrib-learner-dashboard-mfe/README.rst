learner-dashboard-mfe plugin for `Tutor <https://docs.tutor.overhang.io>`__
===========================================================================

This is an experimental plugin (read: it's not supported officially and is not
recommended for production use) that allows Tutor operators to deploy the new
`Learner Dashboard MFE`_.

.. _Learner Dashboard MFE: https://github.com/openedx/frontend-app-learner-dashboard

When enabled, it will replace the existing dashboard for all users.

Installation
------------

This will install the Learner Dashboard plugin directly from Github::

    pip install git+https://github.com/openedx/openedx-tutor-plugins.git#subdirectory=plugins/tutor-contrib-learner-dashboard-mfe

Alternatively, you can clone the parent repository locally and install it from
the checkout::

    git clone https://github.com/openedx/openedx-tutor-plugins.git
    cd openedx-tutor-plugins/plugins/tutor-contrib-learner-dashboard-mfe
    pip install -e .

Usage
-----

Once installed, run the following command to enable the Learner Dashboard
plugin::

    tutor plugins enable learner-dashboard-mfe

If you're using it in an existing local environment, you should also::

    tutor config save
    tutor local do init --limit=dashboard
    tutor images build mfe
    tutor local start mfe -d

Uninstallation
--------------

To uninstall the plugin from an existing local environment::

    tutor local run lms ./manage.py lms waffle_flag --deactivate learner_home_mfe.enabled
    tutor local run lms ./manage.py lms waffle_flag --decativate --everyone learner_recommendations.enable_dashboard_recommendations
    tutor plugins disable learner-dashboard-mfe
    tutor config save
    tutor local restart mfe

Developing
----------

It is possible to use this plugin to develop the Learner Dashboard MFE as per
`the official tutor-mfe instructions`_.  After installing the plugin as
described above, from the parent directory of your Learner Dashboard checkout::

    tutor config save --append MOUNTS=./frontend-app-learner-dashboard
    tutor dev launch

.. _the official tutor-mfe instructions: https://github.com/overhangio/tutor-mfe#mfe-development

License
-------

This software is licensed under the terms of the AGPLv3.
