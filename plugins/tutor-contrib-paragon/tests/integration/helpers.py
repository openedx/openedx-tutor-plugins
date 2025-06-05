"""Helper functions for integration tests of Paragon plugin."""

import subprocess
import logging

logger = logging.getLogger(__name__)

PARAGON_NAME = "paragon"
PARAGON_IMAGE = "paragon-builder"
PARAGON_JOB = "paragon-build-tokens"
PARAGON_THEME_SOURCES_FOLDER = "env/plugins/paragon/theme-sources"
PARAGON_COMPILED_THEMES_FOLDER = "env/plugins/paragon/compiled-themes"


def execute_tutor_command(command: list[str]):
    """Run a Tutor command and return the result.

    Args:
        command (list[str]): List of Tutor args, without the 'tutor' prefix.

    Returns:
        subprocess.CompletedProcess: Contains stdout, stderr, returncode.
    """
    full_command = ["tutor"] + command
    result = subprocess.run(
        full_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        logger.error("Command failed: %s", " ".join(full_command))
        logger.error("stderr: %s", result.stderr.strip())

    return result


def get_tutor_root_path():
    """Get the root path of the Tutor project.

    Raises:
        RuntimeError: If the Tutor root path cannot be obtained.

    Returns:
        str: The path to the Tutor root directory.
    """
    result = execute_tutor_command(["config", "printroot"])

    if result.returncode != 0:
        raise RuntimeError("Failed to get Tutor root path: " + result.stderr)

    return result.stdout.strip()
