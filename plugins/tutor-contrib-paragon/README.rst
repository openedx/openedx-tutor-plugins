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

.. note::

   A link to the official Open edX or Paragon documentation will be added here once it is published.

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
    PARAGON_BUILDER_IMAGE: "paragon-builder:latest"

You may customize paths or theme names to suit your deployment.

Usage
*****

Prerequisites
-------------

- A built Paragon CLI image:

  .. code-block:: bash

      tutor images build paragon-builder

- The ``PARAGON_THEME_SOURCES_PATH`` directory structured as follows:

  .. code-block:: text

      <PARAGON_THEME_SOURCES_PATH>/
      ├── core/
      │   └── ... (token files)
      └── themes/
          ├── light/     # example theme variant
          │   └── ... (light theme token files)
          └── dark/      # example theme variant
          └── ... (dark theme token files)

  In this structure:

  - The ``core/`` directory contains base design tokens common across all themes.
  - The ``themes/`` directory contains subdirectories for each theme variant (e.g., ``light``, ``dark``), each with tokens specific to that theme.

Building Themes
---------------

Invoke the build process via Tutor:

.. code-block:: bash

    tutor local do paragon-build-tokens [OPTIONS]

Available options:

- ``--source-tokens-only``  
  Include only source design tokens in the build.

- ``--output-token-references``  
  Include references for tokens with aliases to other tokens in the build output.

- ``--themes <theme1,theme2>``  
  Comma-separated list of theme names to compile. Defaults to the list defined in ``PARAGON_ENABLED_THEMES`` if not provided.

- ``-v, --verbose``  
  Enable verbose logging.

Examples
--------

.. code-block:: bash

    # Compile all themes listed in PARAGON_ENABLED_THEMES
    tutor local do paragon-build-tokens

    # Compile only specific themes
    tutor local do paragon-build-tokens --themes theme-1,theme-2

    # Compile with full debug logs
    tutor local do paragon-build-tokens --verbose

    # Compile only source tokens for a single theme
    tutor local do paragon-build-tokens --themes theme-1 --source-tokens-only

Output
------

Artifacts will be written to the directory specified by ``PARAGON_COMPILED_THEMES_PATH`` (default: ``env/plugins/paragon/compiled-themes``).

Troubleshooting
***************

- **No custom themes built or only default tokens generated**  
  Ensure that your custom theme directories exist under ``PARAGON_THEME_SOURCES_PATH`` and that their names exactly match those in ``PARAGON_ENABLED_THEMES`` or passed via ``--themes``. If no custom tokens are found, Paragon will fall back to its built-in defaults.

- **Themes are not picked up when using --themes:**  
  The value for ``--themes`` must be a comma-separated list (no spaces), e.g. ``--themes theme-1,theme-2``.

- **Write permission denied**  
  Verify that Docker and the Tutor process have write access to the path defined by ``PARAGON_COMPILED_THEMES_PATH``. Adjust filesystem permissions if necessary.

- **Error: "Expected at least 4 args"**  
  This occurs when the build job is invoked directly inside the container. Always run via Tutor:

  .. code-block:: bash

      tutor local do paragon-build-tokens [OPTIONS]

- **Other issues**  
  Re-run the build with ``--verbose`` to obtain detailed logs and identify misconfigurations or missing files.

License
*******

This software is licensed under the terms of the AGPLv3.
