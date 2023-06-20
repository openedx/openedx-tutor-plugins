from glob import glob
import os
import pkg_resources
import uuid

from tutor import hooks as tutor_hooks
from tutormfe.plugin import MFE_APPS

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

port = 3001

@MFE_APPS.add()
def _add_my_mfe(mfes):
    mfes["library-authoring"] = {
        "repository": "https://github.com/openedx/frontend-app-library-authoring",
        "port": port,
    }
    return mfes

tutor_hooks.Filters.ENV_TEMPLATE_VARIABLES.add_items(
    [("library_authoring_port", port)]
)

tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        ("BLOCKSTORE_COLLECTION_UUID", str(uuid.uuid4()))
    ]
)


########################################
# INITIALIZATION TASKS
########################################

MY_INIT_TASKS: list[tuple[str, tuple[str, ...]]] = [
    ("cms", ("library_authoring_mfe", "jobs", "init", "cms.sh")),
]

# For each task added to MY_INIT_TASKS, we load the task template
# and add it to the CLI_DO_INIT_TASKS filter, which tells Tutor to
# run it as part of the `init` job.
for service, template_path in MY_INIT_TASKS:
    full_path: str = pkg_resources.resource_filename(
        "tutor_library_authoring_mfe", os.path.join("templates", *template_path)
    )
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    tutor_hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))

########################################
# TEMPLATE RENDERING
########################################

tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        pkg_resources.resource_filename("tutor_library_authoring_mfe", "templates"),
    ]
)

########################################
# PATCH LOADING
########################################

# For each file in tutor_library_authoring_mfe/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutor_library_authoring_mfe", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
