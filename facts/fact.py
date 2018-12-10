"""
fact.py - Fact and FactDetail Object Classes

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md

This module is built on top of the Pydle system.
"""

import datetime
from typing import NoReturn


class FactDetail:

    def __init__(self,
                 last_edit: datetime.datetime,
                 last_editor: str,
                 last_content: str
                 ):
        self._last_edit = last_edit
        self._last_editor = last_editor
        self._last_content = last_content


class Fact:

    def __init__(self,
                 name: str,
                 lang: str,
                 content: str,
                 author: str,
                 timestamp: datetime.datetime,
                 details: FactDetail
                 ):
            self._name = name
            self._lang = lang
            self._content = content
            self._author = author
            self._timestamp = timestamp
            self._details = details

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
            Nothing
        """
        if not isinstance(value, str):
            raise TypeError("Expected string value")

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
    def lang(self, value):
        pass
