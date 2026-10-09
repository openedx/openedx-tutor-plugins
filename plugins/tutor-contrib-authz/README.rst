authz plugin for `Tutor <https://docs.tutor.edly.io>`__
#######################################################

Introduction
============

This plugin creates a new Tutor patch point (``openedx-authz-schema``) that lets other plugins contribute authorization schema YAML fragments. All contributions are combined into a single multi-document YAML file and mounted into the LMS/CMS containers at ``/openedx/config/authz-schema.yml``.

A Django setting ``OPENEDX_AUTHZ_SCHEMA_FILES`` is added to ``openedx-common-settings`` so that the ``load_authz_schema`` management command knows where to find the schema files at initialisation time.

Installation
************

.. code-block:: bash

    git clone https://github.com/openedx/openedx-tutor-plugins.git
    cd openedx-tutor-plugins/plugins/tutor-contrib-authz
    pip install -e .

Usage
*****

.. code-block:: bash

    tutor plugins enable authz


Contribute an Authorization Schema
***********************************

1. Create a tutor plugin:

.. code-block:: bash

    touch $(tutor config printroot)-plugins/my_authz_schema.py

2. Use the patch ``openedx-authz-schema`` to contribute your authz schema:

.. code-block:: python

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "openedx-authz-schema",
            """
    schema_version: "1.0"
    priority: 100

    role_extensions:
    - role: course_editor
      add_permissions:
        - courses.export_course
      remove_permissions:
        - courses.manage_tags
      display_name: Course author
      description: Creates and exports course content for this site.

    - role: course_auditor
      hidden: true
            """,
        )
    )

3. Run do init commands:

.. code-block:: bash

    tutor {dev|local|k8s} do init

4. Alternatively, instead of running the do init commands, you can run the following management command for your schemas to be loaded:

.. code-block:: bash

    tutor {dev|local|k8s} exec {cms|lms} ./manage.py load_authz_schema

License
*******

This software is licensed under the terms of the AGPLv3.
