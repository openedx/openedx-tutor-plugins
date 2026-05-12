Portainer plugin for `Tutor <https://docs.tutor.overhang.io>`__
================================================================

This plugin installs `Portainer <https://www.portainer.io/>`_ alongside an
Open edX deployment and exposes its web UI on a dedicated subdomain
(``portainer.<LMS_HOST>`` by default), terminated by Caddy with automatic
TLS.

Installation
------------

Install directly from Github::

    pip install git+https://github.com/openedx/openedx-tutor-plugins.git#subdirectory=plugins/tutor-contrib-portainer

Alternatively, clone the parent repository locally and install it from the
checkout::

    git clone https://github.com/openedx/openedx-tutor-plugins.git
    cd openedx-tutor-plugins/plugins/tutor-contrib-portainer
    pip install -e .

Usage
-----

Enable the plugin and apply the configuration::

    tutor plugins enable portainer
    tutor config save
    tutor local launch

After Portainer comes up, visit ``https://portainer.<LMS_HOST>`` and
follow the first-run wizard to create an admin user. When prompted for
an environment, choose **Local** and Portainer will manage the same
Docker daemon that hosts the Open edX containers.

Configuration
-------------

The plugin exposes the following ``tutor config`` keys:

* ``PORTAINER_HOST`` (default: ``portainer.{{ LMS_HOST }}``) - the
  public hostname Caddy serves the UI on.
* ``PORTAINER_DOCKER_IMAGE`` (default:
  ``docker.io/portainer/portainer-ce:2.41.1-alpine``) - the image used
  for the ``portainer`` service.
* ``PORTAINER_PORT`` (default: ``9000``) - the in-cluster port the
  Portainer container binds to. Caddy reverse-proxies the subdomain
  to this port.

Override any of them with::

    tutor config save --set PORTAINER_HOST=ops.example.com

Data and Docker socket
----------------------

Portainer needs access to the host Docker socket to manage containers,
so this plugin bind-mounts ``/var/run/docker.sock`` into the
``portainer`` service. Persistent data is stored under
``$(tutor config printroot)/data/portainer``.

Granting a container access to the host Docker socket is effectively
equivalent to giving it root on the host. Treat the Portainer admin
credentials accordingly.

Uninstallation
--------------

To disable the plugin::

    tutor plugins disable portainer
    tutor local stop && tutor local start -d

License
-------

This software is licensed under the terms of the AGPLv3.
