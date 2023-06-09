from __future__ import annotations

import os
import os.path
from glob import glob

import pkg_resources

from tutor import hooks
from tutormfe.plugin import MFE_APPS

########################################
# CONFIGURATION
########################################

port = 1996

@MFE_APPS.add()
def _add_my_mfe(mfes):
    mfes["learner-dashboard"] = {
        "repository": "https://github.com/openedx/frontend-app-learner-dashboard",
        "port": port,
    }
    return mfes

hooks.Filters.ENV_TEMPLATE_VARIABLES.add_items(
    [("learner_dashboard_port", port)]
)

########################################
# INITIALIZATION TASKS
########################################

# To add a custom initialization task, create a bash script template under:
# tutor_learner_dashboard_mfe/templates/learner-dashboard-mfe/jobs/init/
# and then add it to the MY_INIT_TASKS list. Each task is in the format:
# ("<service>", ("<path>", "<to>", "<script>", "<template>"))
MY_INIT_TASKS: list[tuple[str, tuple[str, ...]]] = [
    # For example, to add LMS initialization steps, you could add the script template at:
    # tutor_learner_dashboard_mfe/templates/learner-dashboard-mfe/jobs/init/lms.sh
    # And then add the line:
    ### ("lms", ("learner-dashboard-mfe", "jobs", "init", "lms.sh")),
    ("lms", ("learner-dashboard-mfe", "jobs", "init", "lms.sh")),
]


# For each task added to MY_INIT_TASKS, we load the task template
# and add it to the CLI_DO_INIT_TASKS filter, which tells Tutor to
# run it as part of the `init` job.
for service, template_path in MY_INIT_TASKS:
    full_path: str = pkg_resources.resource_filename(
        "tutor_learner_dashboard_mfe", os.path.join("templates", *template_path)
    )
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))


########################################
# PATCH LOADING
########################################

# For each file in tutor_learner_dashboard_mfe/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutor_learner_dashboard_mfe", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
