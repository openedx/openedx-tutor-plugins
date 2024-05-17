# Enable the waffle flag to use this MFE
(./manage.py cms waffle_flag --list | grep studio.library_authoring_mfe) || ./manage.py lms waffle_flag  studio.library_authoring_mfe --create --everyone
