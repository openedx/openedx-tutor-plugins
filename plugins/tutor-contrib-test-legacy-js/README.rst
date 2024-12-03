test-legacy-js plugin for `Tutor <https://docs.tutor.overhang.io>`__
====================================================================

This plugin allows edx-platform developers to run legacy JavaScript tests by adding some system requirements to the ``openedx-dev`` image.

This is a plugin rather than an upstream feature because adding these requirements directly to the core ``openedx-dev`` image would nontrivially increase its size and build time. Only a small minority of edx-platform developers need to run unit tests on the mostly-deprecated legacy JavaScript code.

Installation
------------

This will install the Test Legacy JS plugin directly from Github::

    pip install git+https://github.com/openedx/openedx-tutor-plugins.git#subdirectory=plugins/tutor-contrib-test-legacy-js

Alternatively, you can clone the parent repository locally and install it from the checkout::

    git clone https://github.com/openedx/openedx-tutor-plugins.git
    cd openedx-tutor-plugins/plugins/tutor-contrib-test-legacy-js
    pip install -e .

Usage
-----

Once installed, run the following commands to enable it::

    tutor plugins enable test-legacy-js
    tutor images build openedx-dev

This should allow you to run legacy edx-platform JS tests::

    tutor dev run lms npm run test

License
-------

This software is licensed under the terms of the AGPLv3.
