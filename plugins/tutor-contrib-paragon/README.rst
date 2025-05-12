Paragon plugin for `Tutor <https://docs.tutor.edly.io>`__
###########################################################

Facilitates the generation and static hosting of Paragon-based CSS themes for Open edX Micro-Frontend (MFE) applications using `Paragon <https://openedx.github.io/paragon/>`__.

This plugin provides a local folder structure to manage theme source files and compile them into CSS, enabling flexible customization of Open edX MFEs via Tutor.

Installation
************

.. code-block:: bash

    pip install git+https://github.com/openedx/openedx-tutor-plugins.git#subdirectory=plugins/tutor-contrib-paragon

For development:

.. code-block:: bash

    cd openedx-tutor-plugins/plugins/tutor-contrib-paragon
    pip install -e .

Enable the plugin:

.. code-block:: bash

    tutor plugins enable paragon

Directory Structure
*******************

The plugin will create the following structure inside your Tutor environment:

.. code-block::

    tutor/env/plugins/paragon/
    ├── theme-sources/           # Place your style dictionary folders here (e.g. theme-xyz/)
    └── compiled-themes/         # Compiled CSS files go here, ready for static hosting

Each theme inside `theme-sources/` should follow the Style Dictionary folder structure.
Only themes listed in `PARAGON_ENABLED_THEMES` will be compiled.

The `compiled-themes/` folder is designed to be exposed via static web servers such as **nginx** or **Caddy**, or can be uploaded to cloud hosting providers like **Amazon S3** or **Cloudflare Pages**.

Configuration
*************

All configuration variables can be overridden via `tutor config save`:

.. code-block:: yaml

    PARAGON_THEME_SOURCES_PATH: "env/plugins/paragon/theme-sources"
    PARAGON_COMPILED_THEMES_PATH: "env/plugins/paragon/compiled-themes"
    PARAGON_ENABLED_THEMES:
      - theme-1
      - theme-2
    PARAGON_SERVE_COMPILED_THEMES: true

You may customize paths or theme names to suit your deployment.

License
*******

This software is licensed under the terms of the AGPLv3.