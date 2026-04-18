Google Analytics plugin for `Tutor <https://docs.tutor.overhang.io>`__
=======================================================================

This plugin wires a Google Analytics 4 loader into every Open edX MFE that
is built through ``tutor-mfe``. It duplicates the ``GoogleAnalyticsLoader``
that used to ship with ``@openedx/frontend-platform``.

The loader reads ``GOOGLE_ANALYTICS_4_ID`` from the MFE runtime configuration
(or, for the frontend-base site, from ``commonAppConfig``). When that value
is unset, the loader is a no-op, so the plugin is safe to enable even if
Google Analytics has not yet been configured for a deployment.

Implementation
--------------

The plugin declares a single ``GoogleAnalyticsLoader`` JavaScript class and
inlines it into both build pipelines that tutor-mfe supports. The class
body is injected into ``env.config.jsx`` via the
``mfe-env-config-buildtime-definitions`` patch (for legacy MFEs) and into
``customApp.tsx`` via the ``mfe-site-custom-app-definitions`` patch (for
the frontend-base site). A single ``tutormfe.hooks.EXTERNAL_SCRIPTS``
registration targeting ``"all"`` then wires the class into both: each
legacy MFE's ``externalScripts`` array and the site's
``customApp.externalScripts``.

At runtime, each pipeline instantiates the loader with the relevant app
configuration. Setting ``GOOGLE_ANALYTICS_4_ID`` in the MFE runtime config
(for legacy MFEs) or in ``FRONTEND_SITE_CONFIG['commonAppConfig']`` (for
the frontend-base site) is enough to activate tracking. Without a value,
the loader is a safe no-op.

Installation
------------

Install directly from Github::

    pip install git+https://github.com/openedx/openedx-tutor-plugins.git#subdirectory=plugins/tutor-contrib-google-analytics

Alternatively, clone the parent repository locally and install it from the
checkout::

    git clone https://github.com/openedx/openedx-tutor-plugins.git
    cd openedx-tutor-plugins/plugins/tutor-contrib-google-analytics
    pip install -e .

Usage
-----

Enable the plugin::

    tutor plugins enable google-analytics

Then rebuild the MFE images and restart the environment so the new
``env.config.jsx`` takes effect::

    tutor images build mfe mfe-dev
    tutor local launch

Make sure that ``GOOGLE_ANALYTICS_4_ID`` is present in the MFE runtime
configuration for the deployments where tracking should be active.

Uninstallation
--------------

To disable the plugin::

    tutor plugins disable google-analytics
    tutor local stop && tutor local start -d

License
-------

This software is licensed under the terms of the AGPLv3.
