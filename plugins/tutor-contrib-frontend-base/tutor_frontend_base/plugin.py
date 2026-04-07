from tutormfe.hooks import FRONTEND_APPS


@FRONTEND_APPS.add()
def _enable_core_apps(apps):
    apps["authn"]["enabled"] = True
    apps["learner-dashboard"]["enabled"] = True
    return apps
