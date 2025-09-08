# Set the lti_consumer.enable_external_config_filter waffle flag
./manage.py lms waffle_flag --create --everyone lti_consumer.enable_external_config_filter

# Run migrations for lti_store
./manage.py lms migrate lti_store
