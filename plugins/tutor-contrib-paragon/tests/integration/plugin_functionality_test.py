"""
Integration tests for the Tutor Paragon plugin functionality.

This module contains tests to verify that the Paragon plugin for Tutor
is functioning correctly, including building tokens with and without options,
and handling invalid flags or parameters.
"""

import os

from .helpers import (
    execute_tutor_command,
    get_tutor_root_path,
    PARAGON_JOB,
    PARAGON_COMPILED_THEMES_FOLDER,
)


def test_build_tokens_without_options():
    """
    Verify that running the build-tokens job without additional options
    completes successfully and produces output in the compiled-themes folder.
    """

    result = execute_tutor_command(["local", "do", PARAGON_JOB])
    assert result.returncode == 0, f"Error running build-tokens job: {result.stderr}"

    tutor_root = get_tutor_root_path()
    compiled_path = os.path.join(tutor_root, PARAGON_COMPILED_THEMES_FOLDER)

    contents = os.listdir(compiled_path)
    assert contents, f"No files were generated in {compiled_path}."


def test_build_tokens_with_specific_theme():
    """
    Verify that running the build-tokens job with the --themes option
    for a specific theme (e.g., 'indigo') produces the expected output.
    """
    theme = "indigo"

    result = execute_tutor_command(["local", "do", PARAGON_JOB, "--themes", theme])
    assert result.returncode == 0, f"Error building {theme} theme: {result.stderr}"

    tutor_root = get_tutor_root_path()
    compiled_path = os.path.join(tutor_root, PARAGON_COMPILED_THEMES_FOLDER, "themes")

    entries = os.listdir(compiled_path)
    assert theme in entries, f"'{theme}' theme not found in {compiled_path}."

    theme_path = os.path.join(compiled_path, theme)
    assert os.path.isdir(theme_path), f"Expected {theme_path} to be a directory."
    assert os.listdir(theme_path), f"No files were generated inside {theme_path}."


def test_build_tokens_with_invalid_flag_or_parameter():
    """
    Verify that running the build-tokens job with an invalid flag or parameter
    returns a non-zero exit code.
    """
    result = execute_tutor_command(["local", "do", PARAGON_JOB, "--invalid-flag"])
    assert (
        result.returncode != 0
    ), "Expected non-zero return code when using an invalid flag."
