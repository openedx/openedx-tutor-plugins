"""
Integration tests for the Tutor Paragon plugin functionality.

This module contains tests to verify that the Paragon plugin for Tutor
is functioning correctly, including building tokens with and without options,
and handling invalid flags or parameters.
"""

import os
import shutil
import pytest
import re
import requests
import time

from .helpers import (
    execute_tutor_command,
    get_config_value,
    get_tutor_root_path,
    PARAGON_JOB,
    PARAGON_COMPILED_THEMES_FOLDER,
)


@pytest.fixture(autouse=True)
def clear_compiled_themes_folder():
    """
    Fixture to clear the PARAGON_COMPILED_THEMES_FOLDER after each test.
    """
    yield
    tutor_root = get_tutor_root_path()
    compiled_path = os.path.join(tutor_root, PARAGON_COMPILED_THEMES_FOLDER)
    if os.path.exists(compiled_path):
        shutil.rmtree(compiled_path)


@pytest.mark.order(1)
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


@pytest.mark.order(2)
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


@pytest.mark.order(3)
def test_build_tokens_excluding_core():
    """
    Verify that running the build-tokens job with the --exclude-core option
    excludes the core theme from the output.
    """
    result = execute_tutor_command(["local", "do", PARAGON_JOB, "--exclude-core"])
    assert result.returncode == 0, f"Error excluding core theme: {result.stderr}"

    tutor_root = get_tutor_root_path()
    compiled_path = os.path.join(tutor_root, PARAGON_COMPILED_THEMES_FOLDER)

    entries = os.listdir(compiled_path)
    assert "core" not in entries, "Core theme should be excluded but was found."


@pytest.mark.order(4)
def test_build_tokens_without_output_token_references():
    """
    Ensure that when the build-tokens job is run with --output-references=false,
    the generated variables.css file does not contain any CSS variable references (var(--...)).
    """
    result = execute_tutor_command(
        ["local", "do", PARAGON_JOB, "--output-references=false"]
    )
    assert (
        result.returncode == 0
    ), f"Error running build-tokens with --output-references=false: {result.stderr}"

    tutor_root = get_tutor_root_path()
    compiled_path = os.path.join(tutor_root, PARAGON_COMPILED_THEMES_FOLDER)

    core_variables_css = os.path.join(compiled_path, "core", "variables.css")
    theme_variables_css = os.path.join(compiled_path, "themes", "light", "variables.css")

    assert os.path.exists(core_variables_css), f"{core_variables_css} does not exist."
    assert os.path.exists(theme_variables_css), f"{theme_variables_css} does not exist."

    with open(core_variables_css, "r", encoding="utf-8") as f:
        core_content = f.read()
    with open(theme_variables_css, "r", encoding="utf-8") as f:
        theme_content = f.read()

    token_reference_pattern = re.compile(r"var\(--.*?\)")
    core_references = token_reference_pattern.findall(core_content)
    theme_references = token_reference_pattern.findall(theme_content)

    assert (
        not core_references
    ), f"{core_variables_css} should not contain token references, but found: {core_references}"
    assert (
        not theme_references
    ), f"{theme_variables_css} should not contain token references, but found: {theme_references}"


@pytest.mark.order(5)
def test_build_tokens_with_source_tokens_only():
    """
    Ensure that when the build-tokens job is run with --source-tokens-only,
    the utility-classes.css file is not generated.
    """
    result = execute_tutor_command(["local", "do", PARAGON_JOB, "--source-tokens-only"])
    assert (
        result.returncode == 0
    ), f"Error running build-tokens with --source-tokens-only: {result.stderr}"

    tutor_root = get_tutor_root_path()
    light_theme_path = os.path.join(
        tutor_root, PARAGON_COMPILED_THEMES_FOLDER, "themes", "light"
    )
    utility_classes_css = os.path.join(light_theme_path, "utility-classes.css")

    assert not os.path.exists(
        utility_classes_css
    ), f"{utility_classes_css} should not exist when --source-tokens-only is used."


@pytest.mark.order(6)
def test_build_tokens_generates_minified_bundle():
    """
    Ensure that the build-tokens job generates the minified bundle files for hosting.
    """
    theme = "light"
    result = execute_tutor_command(["local", "do", PARAGON_JOB, "--themes", theme])
    assert result.returncode == 0, f"Error running build-tokens job: {result.stderr}"

    tutor_root = get_tutor_root_path()
    compiled_path = os.path.join(tutor_root, PARAGON_COMPILED_THEMES_FOLDER)

    minified_theme_bundle = os.path.join(
        compiled_path, "themes", theme, f"{theme}.min.css"
    )
    minified_core_bundle = os.path.join(compiled_path, "core", "core.min.css")

    assert os.path.exists(
        minified_core_bundle
    ), f"Minified core bundle file {minified_core_bundle} does not exist."
    assert os.path.exists(
        minified_theme_bundle
    ), f"Minified theme bundle file {minified_theme_bundle} does not exist."


@pytest.mark.order(7)
def test_build_tokens_hosted_files():
    """
    Verify that the compiled themes can be served through the tutor-mfe service.

    This test builds tokens, starts the required services, and checks that the
    static files are accessible via HTTP requests.
    """
    result = execute_tutor_command(["local", "do", PARAGON_JOB])
    assert result.returncode == 0, f"Error running build-tokens job: {result.stderr}"

    static_url_prefix = get_config_value("PARAGON_STATIC_URL_PREFIX").lstrip("/")
    mfe_host = "apps.local.openedx.io"

    services_result = execute_tutor_command(["local", "start", "-d", "caddy", "mfe"])
    assert services_result.returncode == 0, "Error starting hosting services"

    time.sleep(1)

    try:
        base_url = f"http://{mfe_host}/{static_url_prefix}"
        test_files = ["core/core.min.css", "themes/light/light.min.css"]

        for test_file in test_files:
            url = f"{base_url}{test_file}"
            response = requests.get(url, timeout=2)

            assert (
                response.status_code == 200
            ), f"Expected status 200 for {url}, but got {response.status_code}. "

            content_type = response.headers.get("Content-Type", "")
            assert "text/css" in content_type.lower(), (
                f"Expected 'text/css' Content-Type for {url}, but got '{content_type}'."
            )

    finally:
        execute_tutor_command(["local", "stop", "caddy", "mfe"])
