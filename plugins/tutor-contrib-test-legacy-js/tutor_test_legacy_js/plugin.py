from __future__ import annotations

import os
import os.path
from glob import glob

import importlib.resources

from tutor import hooks

########################################
# PATCH LOADING
########################################

# For each file in tutor_test_legacy_js/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        importlib.resources.files("tutor_test_legacy_js") / "patches",
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
