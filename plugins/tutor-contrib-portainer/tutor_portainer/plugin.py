from __future__ import annotations

import os
from glob import glob

from importlib.resources import files
from tutor import hooks as tutor_hooks

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

config: dict[str, dict[str, str | int | bool]] = {
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "docker.io/portainer/portainer-ce:2.41.1-alpine",
        "HOST": "portainer.{{ LMS_HOST }}",
        "PORT": 9000,
    },
}

tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"PORTAINER_{key}", value) for key, value in config["defaults"].items()]
)

########################################
# DOCKER IMAGE MANAGEMENT
########################################

tutor_hooks.Filters.IMAGES_PULL.add_item(
    ("portainer", "{{ PORTAINER_DOCKER_IMAGE }}")
)

########################################
# PUBLIC HOSTS
########################################


@tutor_hooks.Filters.APP_PUBLIC_HOSTS.add()
def _portainer_public_hosts(hosts: list[str], context_name: str) -> list[str]:
    hosts.append("{{ PORTAINER_HOST }}")
    return hosts

########################################
# PATCH LOADING
########################################

patches_dir = files("tutor_portainer") / "patches"
patch_files = glob(
    os.path.join(
        str(patches_dir),
        "*",
    )
)
for path in patch_files:
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(path), patch_file.read())
        )
