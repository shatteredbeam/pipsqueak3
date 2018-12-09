"""
facts_manager.py - Manages access to the central database file

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md

This module is built on top of the Pydle system.
"""

import psycopg2
import datetime
from Modules.database_manager import DatabaseManager
from utils.ratlib import Singleton


# Fact Details Object
class FactDetail:
    last_edit = None
    last_editor = None
    last_content = None

    def __init__(self,
                 last_edit: datetime.datetime,
                 last_editor: str,
                 last_content: str
                 ):
        self.last_edit = last_edit
        self.last_editor = last_editor
        self.last_content = last_content


class Fact:
    name = None
    lang = None
    content = None
    author = None
    timestamp = None
    marked_for_deletion = False
    details = None

    def __init__(self,
                 name: str,
                 lang: str,
                 content: str,
                 author: str,
                 timestamp: datetime.datetime,
                 details: FactDetail
                 ):
            self.name = name
            self.lang = lang
            self.content = content
            self.author = author
            self.timestamp = timestamp
            self.details = details


class FactManager(Singleton):

    # Define our safe tables for FM
    def safe_tables(self):
        return ["fact", "fact_timestamp"]

    def __init__(self):

        # Set our tables for safe_tables

        self.DatabaseManager = DatabaseManager()

