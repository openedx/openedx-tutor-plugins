from __future__ import annotations
from glob import glob
import os
import pkg_resources
import uuid

from tutor import hooks as tutor_hooks

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

tutor_hooks.Filters.CONFIG_DEFAULTS.add_item(
    ("SCOUT_KEY", "")
)
tutor_hooks.Filters.CONFIG_DEFAULTS.add_item(
    ("SCOUT_NAME", "")
)

########################################
# INITIALIZATION TASKS
########################################


########################################
# TEMPLATE RENDERING
########################################


########################################
# PATCH LOADING
########################################

# For each file in tutor_media/patches,
# apply a patch based on the file's name and contents.
patch_files = glob(
    os.path.join(
        pkg_resources.resource_filename("tutor_scout_apm", "patches"),
        "*",
    )
)
for path in patch_files:
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
