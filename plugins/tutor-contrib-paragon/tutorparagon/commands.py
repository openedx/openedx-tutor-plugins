"""
Custom job definitions for the Paragon Tutor plugin.

This module contains Click command definitions that will be registered
as Tutor "do commands", this specialized jobs can be executed using
`tutor local do <command>` or similar.
"""

import click


@click.command(
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True)
)
@click.pass_context
def paragon_build_tokens(ctx: click.Context) -> list[tuple[str, str]]:
    """
    Build theme token files using Paragon.
    Accepts and forwards all options/arguments to paragon-builder.
    """
    return [("paragon-builder", " ".join(ctx.args))]
