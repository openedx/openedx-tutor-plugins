Paragon plugin for `Tutor <https://docs.tutor.edly.io>`__
###########################################################

Facilitates the generation and static hosting of Paragon-based CSS themes for Open edX Micro-Frontend (MFE) applications using `Paragon <https://openedx.github.io/paragon/>`__.

This plugin provides a local folder structure to manage **design token-based theme source files** (see `Paragon Design Tokens <https://github.com/openedx/paragon/?tab=readme-ov-file#design-tokens>`__) and compile them into CSS, enabling flexible customization of Open edX MFEs via Tutor.

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
    ├── theme-sources/           # Place your Paragon-based theme folders here (e.g., theme-xyz/)
    └── compiled-themes/         # Output CSS files are generated here and ready for static hosting

Only themes listed in `PARAGON_ENABLED_THEMES` will be compiled.

Themes placed in `theme-sources/` are compiled into CSS using `Paragon's theme build process <https://github.com/openedx/paragon/?tab=readme-ov-file#paragon-cli>`_. The resulting CSS files in `compiled-themes/` are intended to be served statically and can be linked using the `PARAGON_THEME_URLS` setting.

This structure is optimized for design token–based themes (see `Paragon Design Tokens <https://github.com/openedx/paragon/?tab=readme-ov-file#design-tokens>`__), but it is also flexible. If site operators need to include small amounts of additional CSS (not handled via tokens), we recommend doing so via extensions in the theme source directory, so they are included during the Paragon build—rather than manually editing the compiled output.

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
