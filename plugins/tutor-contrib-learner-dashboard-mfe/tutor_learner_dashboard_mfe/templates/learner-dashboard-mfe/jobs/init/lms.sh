# Enable the waffle flags for this MFE
(./manage.py lms waffle_flag --list | grep learner_home_mfe.enabled) || ./manage.py lms waffle_flag learner_home_mfe.enabled --create --everyone
(./manage.py lms waffle_flag --list | grep learner_recommendations.enable_dashboard_recommendations) || ./manage.py lms waffle_flag learner_recommendations.enable_dashboard_recommendations --create --everyone
