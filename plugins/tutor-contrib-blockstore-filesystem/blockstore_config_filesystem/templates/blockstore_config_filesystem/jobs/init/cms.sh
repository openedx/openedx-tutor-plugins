# Adapted from https://github.com/openedx/frontend-app-library-authoring/blob/26ea285dc2b5f0c32c6f1a9017a45c6add03f8d7/tutor-contrib-library-authoring-mfe/tutor_library_authoring_mfe/templates/library_authoring_mfe/tasks/cms/init
# 
# Create waffle switches to enable the Blockstore app that's now built into
# edx-platform, rather than requiring it to be installed and enabled separately.
(./manage.py cms waffle_switch --list | grep blockstore.use_blockstore_app_api) || ./manage.py lms waffle_switch --create blockstore.use_blockstore_app_api on
