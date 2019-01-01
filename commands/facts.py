"""
facts.py - IRC Commands for the Fact Manager.

Provides IRC commands to manage the Facts database.

Copyright (c) 2018 The Fuel Rat Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md
"""
import logging
import psycopg2

from Modules.context import Context
from Modules.permissions import require_permission, TECHRAT, OVERSEER, RAT, require_channel
from Modules.rat_command import command
from Modules.fact_manager import FactManager, Fact
from datetime import timezone

log = logging.getLogger(f"mecha.{__name__}")


@command("factadd", "fact-add")
@require_permission(OVERSEER)
@require_channel
async def cmd_fm_factadd(context: Context):
    """
    Adds a new fact to the database, with timestamp and invoker as creator,
    creating a transaction log in the process.

    !factadd <name> <langID> <message>
    """
    if len(context.words) == 1:
        await context.reply("Usage: !factadd <name> <lang> <message>")
        return
    else:
        # Build elements for Fact creation
        try:
            fact_name = context.words[1].lower()

            # Check for bad first character (must be a-z)
            if not fact_name[0].isalpha():
                await context.reply("Unable to add fact: Fact name must begin with a-z/A-Z")
                return

            fact_lang = context.words[2].lower()
            # Check for bad first character in lang (must be a-z)
            if not fact_lang[0].isalpha():
                await context.reply("Unable to add fact: Fact langID must begin with a-z/A-Z")
                return

            fact_msg = context.words_eol[3]
            fact_author = context.user.nickname
        except IndexError as error:
            await context.reply("Usage: !factadd <name> <lang> <message>")
            log.warning(f"Malformed factadd request by {context.user.nickname}")
            return

        # Verify that a fact with this name doesn't exist already:
        fm = FactManager()
        if await fm.exists(fact_name, fact_lang):
            await context.reply("That fact already exists.  Use factedit to "
                                "edit an existing fact.")
            return

        # Build Fact, edit date is generated by the class.
        new_fact = Fact(name=fact_name, lang=fact_lang, message=fact_msg,
                        aliases=None, author=fact_author, editedby=fact_author,
                        mfd=False)

        # Do everything in a nice, safe TRY block.
        try:
            await fm.add(new_fact)
        except (psycopg2.DatabaseError, psycopg2.ProgrammingError) as error:
            await context.reply("Unable to add Fact.")
            log.exception(f"Unable to add fact {fact_name} by {fact_author}")
            raise error
        else:
            await context.reply(f"New fact '{fact_name}-{fact_lang}' {fact_msg}")


@command("factdel", "fact-del")
@require_permission(TECHRAT)
async def cmd_fm_factdel(context: Context):
    """
    Deletes a fact marked for deletion, creating a transaction log in the process.

    !factdel <name> <langID>
    """
    await context.reply("Not Yet Implemented. Sorry!")


@command("factalias", "fact-alias")
@require_permission(OVERSEER)
async def cmd_fm_factalias(context: Context):
    """
    Adds/Removes aliases for existing facts.

    !factalias add <base fact> <alias>
    !factalias del <base fact> <alias>
    """
    await context.reply("Not Yet Implemented. Sorry!")


@command("factdetail", "fact-detail")
@require_permission(RAT)
async def cmd_fm_factdetail(context: Context):
    """
    Detailed fact information, per fact.

    !factdetail <name> <langID>
    """
    if len(context.words) != 3:
        await context.reply("Usage: !factdetail <name> <lang>")
        return
    else:
        fact_name = context.words[1].lower()
        fact_lang = context.words[2].lower()

        fm = FactManager()
        if await fm.exists(fact_name, fact_lang):
            fact_result = await fm.find(fact_name, fact_lang)
            fact_edit_time = fact_result.edited.astimezone(timezone.utc).strftime('%d-%m-%Y %H:%M')
            await context.reply(f"Fact Detail for {fact_name}-{fact_lang}:")
            await context.reply(f"Msg: {fact_result.message}")
            await context.reply(f"Last edited by {fact_result.editedby} on {fact_edit_time}")
            await context.reply(f"MFD: {fact_result.mfd}  Aliases: {fact_result.aliases}")
        else:
            await context.reply(f"No fact matching '{fact_name}-{fact_lang}' found.")


@command("factmfd", "fact-mfd")
@require_permission(OVERSEER)
async def cmd_fm_factmfd(context: Context):
    """
    Marks a fact for deletion.
    !factmfd <name> <langID>
    """
    if len(context.words) != 3:
        await context.reply("Usage: !factmfd <name> <lang> "
                            "(Marks or Unmarks a fact for deletion.)")
        return
    else:

        # Get elements from context
        fact_name = context.words[1].lower()
        fact_lang = context.words[2].lower()

        # Verify fact exists
        fm = FactManager()
        if await fm.exists(fact_name, fact_lang):
            if await fm.mfd(fact_name, fact_lang):
                await context.reply(f"Fact '{fact_name}-{fact_lang}' marked for deletion.  "
                                    f"It can no longer be triggered.")
            else:
                await context.reply(f"'{fact_name}-{fact_lang}' "
                                    f"is no longer marked for deletion and can be triggered.")
        else:
            await context.reply(f"No fact matching '{fact_name}-{fact_lang}' found.")
            return


@command("factmfdlist")
@require_permission(OVERSEER)
async def cmd_fm_factmfdlist(context: Context):

    fm = FactManager()
    mfdlist = await fm.mfd_list()

    await context.reply("These facts are marked for deletion:")
    await context.reply(", ".join(mfdlist))


@command("facthistory", "fact-history")
@require_permission(OVERSEER)
async def cmd_fm_facthistory(context: Context):
    """
    Detailed history of fact and revisions.
    !facthistory <name> <langID>
    """
    await context.reply("Not Yet Implemented. Sorry!")
