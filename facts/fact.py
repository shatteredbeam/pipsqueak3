"""
fact.py - Fact and FactDetail Object Classes

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md

This module is built on top of the Pydle system.
"""

import datetime
from typing import NoReturn, Union


class Fact:

    def __init__(self,
                 name: str,
                 lang: str,
                 content: str,
                 author: str,
                 mfd: bool,  # MFD = Marked for deletion
                 created_at: datetime.datetime,
                 last_edit: datetime.datetime,
                 last_editor: str,
                 history: list,
                 ):
            self._name = name
            self._lang = lang
            self._content = content
            self._author = author
            self._created_at = created_at
            self._mfd = mfd
            self._last_edit = last_edit
            self._last_editor = last_editor
            self._history = history

    @property
    def last_edit(self) -> Union[datetime.datetime, None]:
        """
        Timestamp of last edit to fact.
        Returns:
            datetime.datetime OR None if fact has never been edited.
        """
        return self._last_edit

    @last_edit.setter
    def last_edit(self, value) -> NoReturn:
        """
        Sets the last edit date and time.
        Args:
            value: datetime.datetime object for last edited date of the fact.

        Returns:
                Nothing.
        """
        if not isinstance(value, datetime.datetime):
            raise ValueError("Expected datetime.datetime object for timestamp.")

        self._last_edit = value

    @property
    def last_editor(self) -> str:
        """
        String name of the last person to edit the fact.
        Returns:
                str name of last editor
        """
        return self._last_editor

    @last_editor.setter
    def last_editor(self, value) -> NoReturn:
        """
        Sets the last editor of the fact.
        Args:
            value: last editor

        Returns:
                Nothing.
        """
        if not isinstance(value, str):
            raise ValueError("Expected string value for last_editor.")

        self._last_editor = value

    @property
    def history(self) -> list:
        """
        Contains a list of entries extracted from the fact transaction table, ordered by recent.  The first
        parameter is the timestamp.
        Returns:
            list: transaction history for a fact.
        """
        return self._history

    @history.setter
    def history(self, value) -> NoReturn:
        """
        Sets a list of historical transaction items for the fact.
        Args:
            value: List of transaction items.

        Returns:
                Nothing.
        """
        if not isinstance(value, list):
            raise TypeError("Expected list value for history property.")

    @property
    def name(self) -> str:
        """
        Name of Fact, aka triggering command without command prefix.

        Returns:
            Name of the fact, as a string
        """
        return self._name

    @name.setter
    def name(self, value) -> NoReturn:
        """
        Set Fact Name, aka triggering command.
        Args:
            value: string name to be set

        Returns:
                Nothing.
        """
        if not isinstance(value, str):
            raise TypeError("Expected string value for name.")

        self._name = value

    @property
    def lang(self):
        """
        Language ID of the fact. two characters only.

        Returns:
              str language ID.
        """
        return self._lang

    @lang.setter
    def lang(self, value) -> NoReturn:
        """
        Args:
            value: two character language ID of the fact.

        Returns:
                Nothing.
        """
        if not isinstance(value, str):
            raise TypeError("Expected string value for language ID.")

        if not len(value) == 2:
            raise ValueError("Expected length of language ID is 2 characters.")

    @property
    def content(self) -> str:
        """
        Body of Fact return.  'Content' of the fact associated with command/trigger.

        Returns:
                str: Fact.content
        """
        return self._content

    @content.setter
    def content(self, value) -> NoReturn:
        """
        Args:
            value: String value of contents

        Returns:
                Nothing.
        """
        if not isinstance(value, str):
            raise TypeError("expected string value for content")

        self._content = value

    @property
    def author(self) -> str:
        """
        Returns originating author of the fact at initial creation.
        """
        return self._author

    @author.setter
    def author(self, value) -> NoReturn:
        """
        Args:
            value: Author of fact.

        Returns:
                Nothing.
        """
        if not isinstance(value, str):
            raise ValueError("Expected string value for author")

        self._author = value

    @property
    def timestamp(self) -> datetime.datetime:
        """
        This property must ALWAYS be UTC (+0) and/or UTC aware.
        Returns:
            (datetime.datetime) date and time when the fact was added to the database.

        """
        return self._created_at

    @property
    def mfd(self) -> bool:
        """
        A boolean value indicating if the fact is currently marked for deletion. Facts with MFD set
        to TRUE will return as a positive result with factfind.

        Returns:
                True or False.
        """
        return self._mfd

    @mfd.setter
    def mfd(self, value) -> NoReturn:
        """
        Sets the MFD flag for the current fact object.

        Args:
            value: bool to be set.

        Returns:
                Nothing.
        """
        if not isinstance(value, bool):
            raise TypeError("Expected boolean value for MFD property")

        self._mfd = value
