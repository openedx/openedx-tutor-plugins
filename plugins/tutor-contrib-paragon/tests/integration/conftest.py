"""Common fixtures for integration tests."""

import pytest
import subprocess

from .helpers import PARAGON_NAME, PARAGON_IMAGE


@pytest.fixture(scope="package", autouse=True)
def setup_tutor_paragon_plugin():
    """
    Fixture to set up the Tutor Paragon plugin for integration tests.
    This fixture enables the Paragon plugin, builds the necessary Docker image,
    and ensures that the plugin is disabled after the tests are complete.
    """

    subprocess.run(
        ["tutor", "plugins", "enable", PARAGON_NAME],
        check=True,
        capture_output=True,
    )

    subprocess.run(
        ["tutor", "images", "build", PARAGON_IMAGE],
        check=True,
        capture_output=True,
    )

    yield

    subprocess.run(
        ["tutor", "plugins", "disable", PARAGON_NAME],
        check=True,
        capture_output=True,
    )
