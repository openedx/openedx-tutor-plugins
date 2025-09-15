.. _tutor_contrib_paragon:

#####################
Tutor Paragon Plugin
#####################

.. contents:: Table of Contents
   :local:

Introduction
============

What is the Tutor Paragon Plugin?
---------------------------------

The **Tutor Paragon Plugin** (`tutor-contrib-paragon`) enables developers and operators to compile Paragon design tokens into CSS themes using the Paragon CLI and serve those themes to Open edX Micro-Frontends (MFEs) via Tutor.

It wraps the Paragon CLI build process, manages token source directories and output paths, and exposes compiled themes through Tutor's static hosting infrastructure.

What problem does it solve?
---------------------------

This plugin simplifies MFE theme customization by:

* Standardizing how Paragon tokens are compiled.
* Automatically placing output files in a consistent, hostable location.
* Enabling static delivery of CSS files for MFE consumption.
* Supporting tenant-based theme overrides with flexible configuration.

Target Audience
---------------

* Open edX developers customizing MFE themes.
* Operators managing theming at scale.
* Designers experimenting with visual tokens in real-time environments.

Prerequisites
=============

* A working Tutor environment with Docker.
* Familiarity with Paragon design tokens and MFE architecture.
* Basic understanding of Tutor’s plugin system and configuration management.
* Tutor Plugin MFE installed and enabled.


Version Compatibility
=====================

To use this plugin, ensure you're running compatible versions of Open edX and its dependencies:

* **Paragon >= 23**
* **Open edX "Teak" release (Tutor >= 20)**
* **Tutor >= 20**

.. note::

   Design token functionality is available starting from Paragon version 23 and the Open edX "Teak" release (which corresponds to Tutor version 20). While the plugin is expected to support future versions (e.g., Tutor 21+), major releases may introduce breaking changes. Compatibility will be updated as needed.

.. warning::

   As of now, the plugin's `pyproject.toml` specifies `tutor>=19.0.0,<21.0.0`. This constraint may be relaxed once upstream changes in `tutor-mfe` are released (see `overhangio/tutor-mfe#267 <https://github.com/overhangio/tutor-mfe/pull/267>`_ and `overhangio/tutor-mfe#264 <https://github.com/overhangio/tutor-mfe/pull/264>`_).

Installation
============

.. note::
   A future version may be available via PyPI. For now, use the development installation method.

Development Install
-------------------

Clone the repository and install in editable mode:

.. code-block:: bash

    git clone https://github.com/openedx/openedx-tutor-plugins.git
    cd openedx-tutor-plugins/plugins/tutor-contrib-paragon
    pip install -e .

Enable the Plugin
-----------------

Use Tutor to enable the plugin:

.. code-block:: bash

    tutor plugins enable paragon

Verify Installation
-------------------

Check that the plugin is listed and enabled:

.. code-block:: bash

    tutor plugins list | grep paragon

Build the Paragon Image
-----------------------

Before compiling tokens, build the Docker image used by the plugin:

.. code-block:: bash

    tutor images build paragon-builder

Configuration
=============

Core Plugin Settings
--------------------

All configuration variables are defined via Tutor:

+----------------------------+--------------------------------------------------------------+-------------------------------+
| Variable                   | Description                                                  | Default Value                 |
+============================+==============================================================+===============================+
| `PARAGON_THEMES_PATH`     | Base path for theme sources and compiled output              | `env/plugins/paragon/themes` |
+----------------------------+--------------------------------------------------------------+-------------------------------+
| `PARAGON_THEMES`          | List of theme folders to compile and serve                   | `['light', 'dark']`           |
+----------------------------+--------------------------------------------------------------+-------------------------------+
| `MFE_HOST_EXTRA_FILES`    | Whether to serve compiled themes via Tutor’s MFE web server      | `true`                        |
+----------------------------+--------------------------------------------------------------+-------------------------------+

Sample Configuration
--------------------

.. code-block:: yaml

    PARAGON_THEMES_PATH: "{{ TUTOR_ROOT }}/env/plugins/paragon/themes"
    PARAGON_THEMES:
      - light
      - dark
    MFE_HOST_EXTRA_FILES: true

Theme Directory Structure
-------------------------

.. code-block:: text

    {{ TUTOR_ROOT }}/env/plugins/paragon/themes/
    ├── core/           # Shared base design tokens
    ├── light/          # Light theme tokens
    └── dark/           # Dark theme tokens

Only themes listed in `PARAGON_THEMES` will be compiled and served. The `core/` directory is required and provides base styles shared across all themes.

Usage
=====

Build All Themes
----------------

To compile all themes listed in `PARAGON_THEMES`:

.. code-block:: bash

    tutor local do paragon-build-tokens

Build Specific Themes
---------------------

To compile only selected themes:

.. code-block:: bash

    tutor local do paragon-build-tokens --themes light,dark

Pass Additional CLI Options
---------------------------

You can pass extra options to the Paragon CLI:

.. code-block:: bash

    tutor local do paragon-build-tokens --paragon-option value

Output
------

Compiled CSS files (minified `.min.css`) are written to:
{{ TUTOR_ROOT }}/env/plugins/paragon/themes/<theme>/<theme>.min.css

Static Hosting
==============

If `MFE_HOST_EXTRA_FILES` is set to `true`, the plugin:

* Leverages the static file hosting capability provided by the `tutor-mfe` plugin to serve the compiled CSS files.
* Makes the themes accessible via standard static URLs for use in LMS and MFEs.

Example URLs:

* Local LMS: `http://apps.local.openedx.io/static/paragon/themes/light/light.min.css`
* Dev server: `http://localhost:<PORT>/static/paragon/themes/dark/dark.min.css`

Each theme listed in `PARAGON_THEMES` is automatically exposed for use in MFEs.

Updating Theme Configuration
============================

If you make changes to the theme list or other plugin variables, follow these steps to apply them correctly:

1. **Save the new configuration**

Use `tutor config save --set` to update your variables. For example:

.. code-block:: bash

    tutor config save --set PARAGON_THEMES='["light", "dark"]'

2. **Restart the development environment**

After saving the configuration, restart Tutor to apply the changes:

.. code-block:: bash

    tutor dev stop
    tutor dev start

3. **Verify the changes**

Check that the new themes are compiled and served correctly:

.. code-block:: bash

    tutor local do paragon-build-tokens

Loading Base Paragon Styles
===========================

By default, this plugin serves theme-specific CSS files. Micro-Frontends (MFEs) typically include the base Paragon styles (e.g., ``core.min.css``) bundled within their own build. This can lead to users downloading the same base Paragon CSS multiple times as they navigate between different MFEs, impacting performance.

To improve first-load performance and reduce redundant downloads, you can configure your MFEs to load shared base Paragon styles instead.

Ways to use shared base styles:

Option 1: Use jsDelivr CDN
--------------------------

You can configure your MFEs to load base Paragon styles directly from the jsDelivr CDN. This is often the simplest approach.

1.  Determine the ``@openedx/paragon`` version used by your MFEs (e.g., by checking the MFE's ``package.json`` or running ``npm list @openedx/paragon`` within an MFE directory).
2.  Configure your MFE settings (likely via ``MFE_CONFIG`` in Tutor) to use the jsDelivr URL for the base styles.
    *   Example URL: ``https://cdn.jsdelivr.net/npm/@openedx/paragon@23.1.0/dist/core.min.css``
    *   (Replace ``23.1.0`` with the actual version used by your MFEs).

.. note::
   Using jsDelivr involves loading resources from an external CDN. Consider network policies and data privacy requirements before implementing this approach.

Option 2: Host Your Own Base Styles
-----------------------------------

You can host the base Paragon styles yourself using this plugin's static file hosting capability (via ``MFE_HOST_EXTRA_FILES``).

1.  Obtain the base Paragon CSS file (typically ``core.min.css``) for the version(s) used by your MFEs.
2.  Place the base CSS file(s) into your ``PARAGON_THEMES_PATH`` directory. A common structure might be:
    .. code-block:: text

       {{ TUTOR_ROOT }}/env/plugins/paragon/themes/
       └── core/
           └── 23.1.0/ # Use the actual Paragon version
               └── core.min.css

3.  Configure your MFEs to load the base styles from the plugin's static URL.
    *   Example URL (based on the structure above): ``http://<your-lms-domain>/static/paragon/themes/core/23.1.0/core.min.css``
    *   Replace ``<your-lms-domain>`` with your actual LMS domain (e.g., ``apps.local.openedx.io``).
    *   Update your MFE configuration (for example, by setting ``MFE_CONFIG["PARAGON_THEME_URLS"]`` in your Tutor settings) to point to this URL. **This URL must be placed under the ``"default"`` key within the ``"core"`` section.**
    *   Example configuration snippet:

        .. code-block:: python

            MFE_CONFIG["PARAGON_THEME_URLS"] = {
                "core": {
                    "urls": {
                        "default": "http://<your-lms-domain>/static/paragon/themes/core/23.1.0/core.min.css"
                    },
                },
                # ... other configurations for variants
            }

.. note::
   When hosting your own base styles, ensure the versions match those expected by your MFEs. Using a single, compatible version (e.g., the latest minor of the major version used) is often sufficient if you are using standard MFEs from the same Open edX release. For advanced configurations like version wildcards, refer to the `frontend-platform theming documentation <https://github.com/openedx/frontend-platform/blob/master/docs/how_tos/theming.md>`_.

Additional Resources
--------------------

For more detailed information on MFE theming and loading external styles, refer to the `frontend-platform theming documentation <https://github.com/openedx/frontend-platform/blob/master/docs/how_tos/theming.md>`_.

Troubleshooting
===============

* **Themes not compiled**: Ensure theme folders exist and match names in `PARAGON_THEMES`.
* **Permission errors**: Verify Docker and Tutor have write access to the themes directory.
* **Missing core tokens**: Ensure the `core/` folder exists and contains valid token files.
* **Error: "Expected at least 4 args"**: Always run builds via `tutor local do`, not inside containers.
* **Other issues**: Re-run with `--verbose` for detailed logs.

License
=======

This software is licensed under the terms of the **AGPLv3**.
