"""
case_commands.py - provides case management commands for IRC interaction.

Copyright (c) 2018 The Fuel Rat Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md
"""
import logging

from src.packages.rescue.rat_rescue import Rescue, Rat
from src.packages.board.board import RatBoard
from src.packages.commands import command
from src.packages.context import Context
from src.packages.utils import Status, Platforms, Formatting
from src.packages.permissions.permissions import require_channel, require_dm, require_permission, RAT, TECHRAT, \
    OVERSEER, ADMIN



LOG = logging.getLogger(f"mecha.{__name__}")


@require_channel
@require_permission(RAT)
@command('active', 'activate', 'inactive', 'deactivate')
async def cmd_case_management_active(ctx: Context):
    """
    Toggles the indicated case as active or inactive.  Requires the case is open.

    Usage: !active 2|RatClientName

    Channel Only: YES
    Permission: Rat
    """
    if len(ctx.words) != 2:
        await ctx.reply("Usage: !active <Client Name|Board Index>")

    rescue = ctx.bot.board.get(ctx.words[1])

    if rescue not in ctx.bot.board:
        return await ctx.reply("No Open case with that number or client.")

    with ctx.bot.board.get(rescue) as case:
        case.active = not case.active
        await ctx.reply(f'{case.client}\'s case  is now {Formatting.FORMAT_BOLD} '
                        f'{"Active" if case.active else "Inactive"}.')


@require_channel
@require_permission(RAT)
@command('assign', 'add', 'go', 'gocr')
async def cmd_case_management_assign(ctx: Context):
    """
    Assigns a rat to a case in progress.

    Channel Only: YES
    Permission:  Rat
    """
    ...
    # TODO: API required


@require_channel
@require_permission(RAT)
@command('close', 'clear')
async def cmd_case_management_close(ctx :Context):
    ...