"""
Integration tests for the Tutor Paragon plugin setup.

This module contains tests to verify that the Paragon plugin for Tutor
is correctly installed, enabled, and has the expected directory structure
and jobs available in the system.
"""

from .helpers import (
    execute_tutor_command,
    get_tutor_root_path,
    PARAGON_NAME,
    PARAGON_JOB,
    PARAGON_COMPILED_THEMES_FOLDER,
    PARAGON_THEME_SOURCES_FOLDER,
)

import logging
import os

logger = logging.getLogger(__name__)


def test_paragon_plugin_installed():
    """Verify that the 'paragon' plugin is installed and enabled."""

    plugins_list_cmd = ["plugins", "list"]
    result = execute_tutor_command(plugins_list_cmd)

    assert result.returncode == 0, f"Error listing plugins: {result.stderr}"
    assert (
        PARAGON_NAME in result.stdout
    ), f"The '{PARAGON_NAME}' plugin is not installed"
    assert "enabled" in result.stdout, f"The '{PARAGON_NAME}' plugin is not enabled"


def test_paragon_plugin_folders_created():
    """Verify that the 'paragon' plugin's folders exist in the filesystem."""

    project_root = get_tutor_root_path()

    folders_to_check = [
        PARAGON_THEME_SOURCES_FOLDER,
        PARAGON_COMPILED_THEMES_FOLDER,
    ]

    for folder in folders_to_check:
        folder_path = f"{project_root}/{folder}"

        assert os.path.exists(folder_path), f"Folder {folder_path} does not exist."
        assert os.path.isdir(folder_path), f"{folder_path} is not a directory."


def test_paragon_plugin_build_tokens_job_exists():
    """Verify that the 'paragon-build-tokens' job exists in Tutor's configuration."""

    jobs_list_cmd = ["local", "do", "-h"]
    result = execute_tutor_command(jobs_list_cmd)

    assert result.returncode == 0, f"Error listing jobs: {result.stderr}"
    assert PARAGON_JOB in result.stdout, f"Job '{PARAGON_JOB}' does not exist"
