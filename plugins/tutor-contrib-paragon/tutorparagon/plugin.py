import os
from glob import glob

import click
import importlib_resources
from tutor import hooks
from tutor import config as tutor_config

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Plugin version (used for compatibility or debugging)
        ("PARAGON_VERSION", __version__),
        # Directory where users will place style-dictionary source files
        # Each subfolder inside will represent a theme (e.g., "theme-abc/")
        ("PARAGON_THEME_SOURCES_PATH", "env/plugins/paragon/theme-sources"),
        # Directory where compiled CSS themes will be stored after transformation
        # One subfolder per compiled theme (e.g., "theme-abc/core.min.css")
        ("PARAGON_COMPILED_THEMES_PATH", "env/plugins/paragon/compiled-themes"),
        # List of enabled themes to compile and serve
        # Only themes listed here will be processed, even if others exist in sources
        ("PARAGON_ENABLED_THEMES", []),
        # Whether Tutor should expose the compiled themes to be served (e.g. via nginx, cady or static server)
        ("PARAGON_SERVE_COMPILED_THEMES", True),
        # Paragon Builder Docker image
        # This image is used to compile themes and should be built with `tutor images build paragon-builder`
        ("PARAGON_BUILDER_IMAGE", "paragon-builder:latest"),
    ]
)


# Create directories for build and host
@hooks.Actions.PROJECT_ROOT_READY.add()
def create_paragon_folders(project_root: str) -> None:
    config = tutor_config.load(project_root)

    # Paths from config (always have defaults)
    theme_sources_path = os.path.join(
        project_root, str(config["PARAGON_THEME_SOURCES_PATH"])
    )
    compiled_themes_path = os.path.join(
        project_root, str(config["PARAGON_COMPILED_THEMES_PATH"])
    )

    for path, label in [
        (theme_sources_path, "Theme Sources"),
        (compiled_themes_path, "Compiled Themes"),
    ]:
        if os.path.exists(path):
            print(f"[paragon] {label} folder already exists at: {path}")
        else:
            os.makedirs(path, exist_ok=True)
            print(f"[paragon] Created {label} folder at: {path}")


########################################
# DOCKER IMAGE MANAGEMENT
########################################

hooks.Filters.IMAGES_BUILD.add_items(
    [
        (
            "paragon-builder",  # Image name used with 'tutor images build myservice'
            ("plugins", "paragon", "build", "paragon-builder"),  # Path to Dockerfile
            "{{ PARAGON_BUILDER_IMAGE }}",  # Docker image tag
            (),  # Build arguments
        ),
    ]
)


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        str(importlib_resources.files("tutorparagon") / "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``tutorparagon/templates/paragon/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/paragon/build``.
    [
        ("paragon/build", "plugins"),
        ("paragon/apps", "plugins"),
    ],
)


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutorparagon/patches,
# apply a patch based on the file's name and contents.
for path in glob(str(importlib_resources.files("tutorparagon") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))


########################################
# CUSTOM JOBS (a.k.a. "do-commands")
########################################


@click.command()
@click.option(
    "--source-tokens-only",
    is_flag=True,
    default=False,
    help="Include only source design tokens in the build.",
)
@click.option(
    "--output-token-references",
    is_flag=True,
    default=False,
    help="Include references for tokens with aliases to other tokens in the build output.",
)
@click.option("--themes", help="Comma-separated list of themes to build.")
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Enable verbose logging."
)
def build_tokens(
    themes: str,
    source_tokens_only: bool,
    output_token_references: bool,
    verbose: bool,
) -> list[tuple[str, str]]:
    """
    Build theme token files using Paragon.

    Args:
        source_tokens_only (bool): Only source design tokens.
        output_token_references (bool): Output token references.
        themes (str): Comma-separated list of themes.
        verbose (bool): Verbose logging.

    Returns:
        list[tuple[str, str]]: List of commands to run.
    """
    args = []
    if source_tokens_only:
        args.append("--source-tokens-only")
    if output_token_references:
        args.append("--output-token-references")
    if themes:
        args.append("--themes")
        args.append(themes)
    if verbose:
        args.append("--verbose")

    return [("paragon-builder", " ".join(args))]


hooks.Filters.CLI_DO_COMMANDS.add_item(build_tokens)
