.. _tutor_contrib_paragon:

#####################
Tutor Paragon Plugin
#####################

.. contents:: Tabla de Contenidos
   :local:

Introduction
============

What is the Tutor Paragon Plugin?
---------------------------------

The Tutor Paragon Plugin (``tutor-contrib-paragon``) enables developers and operators to compile design tokens into CSS themes using the Paragon CLI and serve those themes to Open edX Micro-Frontends (MFEs) via Tutor.

This plugin introduces a wrapper around the Paragon CLI build process, managing token source directories and output paths, and exposing compiled themes through Tutor's static hosting infrastructure.

What problem does it solve?
---------------------------

This plugin simplifies the theme customization process across MFEs by:

*   Standardizing how Paragon tokens are compiled.
*   Automatically placing output files in a consistent, hostable location.
*   Enabling static delivery of CSS files for MFE consumption.
*   Allowing tenant-based theme overrides with flexible configuration.

Target Audience
---------------

*   Open edX developers customizing MFE themes.
*   Operators managing theming at scale.
*   Designers experimenting with visual tokens in real-time environments.

Prerequisites
=============

*   Working Tutor environment with Docker.
*   Familiarity with Paragon design tokens and MFE architecture.
*   Basic understanding of Tutor plugin system and configuration management.

Version Compatibility
=====================

To use the Tutor Paragon Plugin, ensure you are running compatible versions of the Open edX platform and its dependencies:

* **Paragon 23+**
* **Open edX "Teak" release (or Tutor 20+)**
* **Tutor 20+**

.. note::
   Design tokens functionality, which this plugin relies on, is available starting from Paragon version 23 and the Open edX "Teak" release (which corresponds to Tutor version 20). Using this plugin with earlier versions may result in compatibility issues or missing features.

Installation
============

.. note::
   A future version of this plugin may be available for installation via PyPI. For now, please use the development installation method below.

Development Install
-------------------

Clone the repo and install in editable mode:

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

You should see something like:

.. code-block:: text

    paragon         enabled

If the plugin appears as 'enabled', it's ready to use.
Ensure the plugin is listed in Tutor:

.. code-block:: bash

    tutor plugins list

Build the Paragon Image
-----------------------

Before compiling tokens, build the image used by the plugin:

.. code-block:: bash

    tutor images build paragon-builder

Configuration
=============

Core Plugin Settings
--------------------

All configuration variables are defined via Tutor:

*   ``PARAGON_THEME_SOURCES_PATH``: Location of your token input folders.
*   ``PARAGON_COMPILED_THEMES_PATH``: Output folder for generated CSS.
*   ``PARAGON_ENABLED_THEMES``: List of themes to compile.
*   ``PARAGON_SERVE_COMPILED_THEMES``: Whether to host the compiled files.

Sample Configuration
--------------------

.. code-block:: yaml

    PARAGON_THEME_SOURCES_PATH: "{{ TUTOR_ROOT }}/env/plugins/paragon/theme-sources"
    PARAGON_COMPILED_THEMES_PATH: "{{ TUTOR_ROOT }}/env/plugins/paragon/compiled-themes"
    PARAGON_ENABLED_THEMES:
      - light
      - dark
    PARAGON_SERVE_COMPILED_THEMES: true

Theme Directory Structure
-------------------------

.. code-block:: text

    theme-sources/
    ├── core/
    │   └── base tokens
    └── themes/
        ├── light/
        └── dark/

The ``core`` directory contains shared design tokens. Each theme in ``themes/`` is compiled into separate CSS files.

Usage
=====

Compiling Themes
----------------

This plugin wraps the ``npx paragon build-tokens`` command. To compile themes:

.. code-block:: bash

    tutor local do paragon-build-tokens

By default, it uses the themes defined in ``PARAGON_ENABLED_THEMES``.

Options
-------

The Tutor Paragon plugin acts as a wrapper for the Paragon CLI. It forwards any flags or options you provide directly to the underlying ``paragon build-tokens`` command. This means you can use all the options available in the `Paragon CLI documentation <https://github.com/openedx/paragon>`_.

Common options include:

*   ``--themes``: comma-separated list of themes to compile.
*   ``--paragon-option``: pass any custom flag to Paragon CLI.

For a complete list of available flags and their descriptions, please refer to the `Paragon CLI documentation <https://github.com/openedx/paragon>`_.

Examples
--------

.. code-block:: bash

    tutor local do paragon-build-tokens --themes light,dark

Output
------

CSS files will be placed in:

``{{ TUTOR_ROOT }}/env/plugins/paragon/compiled-themes/<theme>/theme.css``

These are served statically when ``PARAGON_SERVE_COMPILED_THEMES`` is enabled.

.. note::

   If no themes are configured, the plugin falls back to Paragon's built-in light theme.

Integration with MFEs
=====================

Serving CSS Themes
------------------

.. note::

   The plugin hosts only the **minified versions** of the CSS files generated by Paragon. These files have the ``.min.css`` extension (e.g., ``<theme-name>.min.css``).

In development, use localhost directly because there is no reverse proxy:

``http://localhost:8000/static/paragon/<theme>.min.css``

In production, the LMS and Caddy proxy handle requests automatically, so the files are served at:

``https://<LMS_DOMAIN>/static/paragon/<theme>.min.css``

Compiled themes are available at:

*   **Development:** ``http://localhost:8000/static/paragon/<theme>.min.css``
*   **Production:** ``<LMS_URL>/static/paragon/<theme>.min.css``

Using in MFEs
-------------

Include the CSS link in your MFE HTML shell:

.. code-block:: html

    <link rel="stylesheet" href="/static/paragon/light.min.css" />

Multi-Tenant Support
--------------------

The plugin is designed to support multi-tenant environments. The core configuration can be overridden on a per-tenant basis, allowing for different themes to be served to different tenants. Specific integration details with tenant management systems (like ``eox-tenant``) will be documented separately.

Testing and Validation
======================

To verify that everything works:

1.  Build tokens: ``tutor local do paragon-build-tokens``
2.  Start the environment: ``tutor local start -d``
3.  Open the URL: ``http://localhost:8000/static/paragon/light.min.css``
4.  If the CSS loads in the browser, hosting is working correctly.

Verify Output
-------------

After building, check this directory:

.. code-block:: bash

    ls {{ TUTOR_ROOT }}/env/plugins/paragon/compiled-themes/

You should see:

*   ``core.css``
*   ``<theme>.min.css``

Verbose Logging
---------------

Run with:

.. code-block:: bash

    tutor local do paragon-build-tokens --verbose

Troubleshooting
===============

No Custom Tokens Built
----------------------

Check that the theme directory names match ``PARAGON_ENABLED_THEMES``. Paragon will fall back to its default theme if none are found.

Themes Not Compiled
-------------------

Use ``--themes`` with no spaces:

.. code-block:: bash

    tutor local do paragon-build-tokens --themes theme-1,theme-2

Permission Denied
-----------------

Ensure Docker and Tutor can write to the paths.

"Expected at least 4 args" Error
--------------------------------

Only run builds with:

.. code-block:: bash

    tutor local do paragon-build-tokens

Contributing
============

Repository
----------

The main repository for this plugin is located at: https://github.com/openedx/openedx-tutor-plugins/tree/main/plugins/tutor-contrib-paragon

Local Development
-----------------

Clone the repo and install in editable mode:

.. code-block:: bash

    git clone https://github.com/openedx/openedx-tutor-plugins.git
    cd openedx-tutor-plugins/plugins/tutor-contrib-paragon
    pip install -e .

PR Process
----------

1.  Fork the repository.
2.  Create a feature branch.
3.  Submit a pull request.
4.  Follow project guidelines and include tests where applicable.

License and Credits
===================

License
-------

This plugin is licensed under the AGPLv3.

Credits
-------

Developed by edunext, with inspiration from Tutor and Paragon tooling.
For issues or support, open a GitHub issue or contact the maintainers.
