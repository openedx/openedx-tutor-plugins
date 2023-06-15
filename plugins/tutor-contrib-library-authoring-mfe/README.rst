library_authoring_mfe plugin for `Tutor <https://docs.tutor.overhang.io>`_
===================================================================================

Installation
------------

Follow these instructions to enable this microfrontend:

* Install `tutor <https://github.com/overhangio/tutor/>`_ and `tutor-mfe <https://github.com/overhangio/tutor-mfe/>`_: ``pip install tutor tutor-mfe``
* To use blockstore with `minio <https://min.io/>`_
  
  * Install `tutor-minio <https://github.com/overhangio/tutor-minio>`_ ``pip install tutor-minio``
  * Enable minio plugin: ``tutor plugins enable minio``
  * Enable the blockstore-minio plugin: ``tutor plugins enable blockstore-minio``

* To use blockstore with django :code:`FileSystemStorage`

  * Enable the blockstore-filesystem plugin: ``tutor plugins enable blockstore-filesystem``

* Enable this plugin: ``tutor plugins enable library-authoring-mfe``
* Save the tutor config: ``tutor config save``
* Build mfe image: ``tutor images build mfe`` (if you have trouble here you may need to run it with ``--no-cache``) 
* Launch tutor: ``tutor local launch``

If you want to run this MFE in
`development mode <https://github.com/overhangio/tutor-mfe/#mfe-development>`_
(to make changes to the code), instead of step 9 above, do this::

   tutor config save --append MOUNTS=./frontend-app-library-authoring
   cd frontend-app-library-authoring
   nvm use && npm install
   tutor dev launch

Setup
-----
* Ensure you have created a user: https://docs.tutor.overhang.io/local.html#creating-a-new-user-with-staff-and-admin-rights
* Ensure you have created an organization: http://studio.local.overhang.io/admin/organizations/organization/
* If you're using minio

  * Log in to the `minio Web UI <http://minio.local.overhang.io>`_ (`instructions to find credentials <https://github.com/overhangio/tutor-minio#web-ui>`_)
  * Create a **public** bucket for blockstore (the default configuration expects the bucket to be named :code:`blockstore`)

Usage
-----
* Log in to studio: http://studio.local.overhang.io/home/
* Click on the libraries tab
