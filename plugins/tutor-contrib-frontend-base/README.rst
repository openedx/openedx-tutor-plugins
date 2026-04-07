frontend-base plugin for `Tutor <https://docs.tutor.overhang.io>`__
====================================================================

This is a very simple plugin.  It's only job is to enable the `frontend-base
<https://github.com/openedx/frontend-base>`__ core apps already present in
Tutor via `tutor-mfe <https://github.com/overhangio/tutor-mfe>`__.

Frontend-base is a unified framework that replaces ``frontend-build``,
``frontend-platform``, ``frontend-plugin-framework``,
``frontend-component-header``, and ``frontend-component-footer``. It enables
frontend apps to be loaded as direct plugins within a single shell application,
rather than as separate, independently deployed micro frontends.

When enabled, this plugin activates the two core frontend apps that ship with
tutor-mfe: ``authn`` and ``learner-dashboard``. Because these match existing
legacy MFEs, the legacy versions are effectively disabled in favor of their
frontend-base counterparts.

Installation
------------

This plugin requires the ``frontend-base`` branch of tutor-mfe, which has not
yet been released. Install it first::

    pip install "git+https://github.com/overhangio/tutor-mfe.git@frontend-base"

After installing the tutor-mfe ``frontend-base`` branch, the ``mfe`` and
``mfe-dev`` images need to be rebuilt::

    tutor images build mfe mfe-dev

Then install this plugin directly from Github::

    pip install git+https://github.com/openedx/openedx-tutor-plugins.git#subdirectory=plugins/tutor-contrib-frontend-base

Alternatively, you can clone the parent repository locally and install it from
the checkout::

    git clone https://github.com/openedx/openedx-tutor-plugins.git
    cd openedx-tutor-plugins/plugins/tutor-contrib-frontend-base
    pip install -e .

Usage
-----

Once installed, enable the plugin::

    tutor plugins enable frontend-base

After this, restart or launch your environment::

    tutor local launch

After this, the frontend-base version of the Open edX frontend should be accessible.

Uninstallation
--------------

To disable the plugin::

    tutor plugins disable frontend-base
    tutor local stop && tutor local start -d

License
-------

This software is licensed under the terms of the AGPLv3.
