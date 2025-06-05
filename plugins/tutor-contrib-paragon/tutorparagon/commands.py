"""
Custom job definitions for the Paragon Tutor plugin.

This module contains Click command definitions that will be registered
as Tutor "do commands", this specialized jobs can be executed using
`tutor local do <command>` or similar.
"""

import click


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
def paragon_build_tokens(
    source_tokens_only: bool,
    output_token_references: bool,
    themes: str,
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
