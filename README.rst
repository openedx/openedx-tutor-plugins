openedx-tutor-plugins
#####################

|license-badge| |status-badge|

.. |license-badge| image:: https://img.shields.io/github/license/openedx/openedx-tutor-plugins.svg
    :target: https://github.com/openedx/openedx-tutor-plugins/blob/main/LICENSE
    :alt: License

.. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen

Purpose
=======

This repository houses a collection of Tutor plugins maintained by the Open edX
community:

===================================  ======================================================
Plugin                               Status (*Experimental*, *Production*, or *Deprecated*)
===================================  ======================================================
tutor-contrib-learner-dashboard-mfe  Experimental
tutor-contrib-library-authoring-mfe  Experimental
tutor-contrib-blockstore-filesystem  Experimental
tutor-contrib-blockstore-minio       Experimental
===================================  ======================================================

Getting Started
===============

Generally, assuming `Tutor is installed`_, to add a plugin in this repository
to your deployment environment you would:

.. code:: bash
	  
	  git clone git@github.com:openedx/openedx-tutor-plugins
          cd openedx-tutor-plugins/plugins/<plugin-name>
          pip install -e .
          tutor plugins enable <plugin-name>
          tutor config save

Make sure to check each plugin's README file for more details.

.. _Tutor is installed: https://docs.tutor.overhang.io/install.html

Developing
==========

To create a new Tutor plugin in this repository, use the `Tutor plugin
cookiecutter`_ in a directory under `plugins`, and commit results.

.. _Tutor plugin cookiecutter: https://github.com/overhangio/cookiecutter-tutor-plugin

Getting Help
============

If you're having trouble, we have discussion forums at
https://discuss.openedx.org where you can connect with others in the community.

Our real-time conversations are on Slack. You can request a `Slack
invitation`_, then join our `community Slack workspace`_.  And because this is
a Tutor plugin repository, the best place to discuss it would be in the `#tutor
channel`_.

For anything non-trivial, the best path is to open an issue in this repository
with as many details about the issue you are facing as you can provide.

https://github.com/openedx/openedx-tutor-plugins/issues

For more information about these options, see the `Getting Help`_ page.

.. _Slack invitation: https://openedx.org/slack
.. _community Slack workspace: https://openedx.slack.com/
.. _#tutor channel: https://openedx.slack.com/archives/CGE253B7V
.. _Getting Help: https://openedx.org/getting-help

License
=======

The code in this repository is licensed under the AGPLv3 unless otherwise
noted.

Please see `LICENSE <LICENSE>`_ for details.

Contributing
============

Contributions are very welcome.  Please read `How To Contribute`_ for details.

.. _How To Contribute: https://openedx.org/r/how-to-contribute

This project is currently accepting all types of contributions, bug fixes,
security fixes, maintenance work, or new features.  However, please make sure
to have a discussion about your new feature idea with the maintainers prior to
beginning development to maximize the chances of your change being accepted.
You can start a conversation by creating a new issue on this repo summarizing
your idea.

The Open edX Code of Conduct
============================

All community members are expected to follow the `Open edX Code of Conduct`_.

.. _Open edX Code of Conduct: https://openedx.org/code-of-conduct/

People
======

The assigned maintainers for this component and other project details may be
found in `Backstage`_. Backstage pulls this data from the ``catalog-info.yaml``
file in this repo.

.. _Backstage: https://open-edx-backstage.herokuapp.com/catalog/default/component/openedx-tutor-plugins

Reporting Security Issues
=========================

Please do not report security issues in public, and email security@openedx.org instead.
