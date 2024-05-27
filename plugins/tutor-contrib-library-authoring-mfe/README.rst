library_authoring_mfe plugin for `Tutor <https://docs.tutor.overhang.io>`_
===================================================================================

Installation
------------

Follow these instructions to enable this microfrontend:

* Install `tutor <https://github.com/overhangio/tutor/>`_ and `tutor-mfe <https://github.com/overhangio/tutor-mfe/>`_: ``pip install tutor tutor-mfe``
* Install the library-authoring-mfe plugin: ``pip install git+https://github.com/openedx/openedx-tutor-plugins#subdirectory=plugins/tutor-contrib-library-authoring-mfe``
* Enable this plugin: ``tutor plugins enable library-authoring-mfe``

* You can do one of the following steps depending on how you want to use this mfe:

  If you want to run this MFE in `development mode <https://github.com/overhangio/tutor-mfe/#mfe-development>`_ (to make changes to the code),
  do this::

   tutor config save --append MOUNTS=./frontend-app-library-authoring

   git clone https://github.com/openedx/frontend-app-library-authoring.git

   cd frontend-app-library-authoring

   nvm use && npm install

   tutor dev launch

  If you do not want to run this MFE in `development mode <https://github.com/overhangio/tutor-mfe/#mfe-development>`_ do this:

    Save the tutor config: ``tutor config save``
* Build mfe image: ``tutor images build mfe`` (if you have trouble here you may need to run it with ``--no-cache``)
* Launch tutor: ``tutor local launch``

Setup
-----
* Ensure you have created a user: https://docs.tutor.overhang.io/local.html#creating-a-new-user-with-staff-and-admin-rights
* Ensure you have created an organization: http://studio.local.overhang.io/admin/organizations/organization/

Usage
-----
* Log in to studio: http://studio.local.overhang.io/home/
* Click on the libraries tab
