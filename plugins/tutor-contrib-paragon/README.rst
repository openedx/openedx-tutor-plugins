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

* **Paragon 23+**
* **Open edX "Teak" release (or Tutor 20+)**
* **Tutor 20+**

.. note::
   Design token functionality is available starting from Paragon 23 and Open edX "Teak". Earlier versions may not be compatible.

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

* Local LMS: `http://local.openedx.io/static/paragon/themes/light/light.min.css`
* Dev server: `http://localhost:<PORT>/static/paragon/themes/dark/dark.min.css`

Each theme listed in `PARAGON_THEMES` is automatically exposed for use in MFEs.

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
