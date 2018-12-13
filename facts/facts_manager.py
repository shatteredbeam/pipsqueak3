"""
facts_manager.py - Manages fact storage and retrieval.

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md

This module is built on top of the Pydle system.
"""


import logging
import psycopg2
from psycopg2 import sql
from facts import Fact, FactDetail, FactManager, DatabaseManager
from typing import NoReturn, Optional
from utils.ratlib import Singleton

log = logging.getLogger(f"mecha.{__name__}")


class FactManager(Singleton):
    _SELECT_FACT = ''
    _UPDATE_FACT = ''
    _INSERT_FACT = ''
    _CREATE_FACT_DETAIL_TABLE = 'CREATE TABLE IF NOT EXISTS fact_detail ' \
                                '(id SERIAL, fact_name VARCHAR NOT NULL, ' \
                                'fact_lang VARCHAR NOT NULL, ' \
                                'last_edit TIMESTAMP WITH TIME ZONE, ' \
                                'last_editor VARCHAR NOT NULL, ' \
                                'mfd BOOLEAN NOT NULL, ' \
                                'PRIMARY KEY (id), FOREIGN KEY (fact_name, fact_lang) ' \
                                'REFERENCES fact (name, lang))'
    _CREATE_FACT_TRANSACTION_TABLE = 'CREATE TABLE IF NOT EXISTS fact_transaction ' \
                                     '(id SERIAL, fact_name VARCHAR NOT NULL, ' \
                                     'fact_lang VARCHAR NOT NULL, changed_from VARCHAR, ' \
                                     'changed_to VARCHAR, author VARCHAR NOT NULL, ' \
                                     'date_changed TIMESTAMP WITH TIME ZONE NOT NULL, ' \
                                     'PRIMARY KEY (id), FOREIGN KEY (fact_name, fact_lang) ' \
                                     'REFERENCES fact (name, lang))'

    # Define our safe tables for FM
    def safe_tables(self):
        return ["fact", "fact_detail", "fact_transaction"]

    def __init__(self):

        # Singleton Check
        if not hasattr(self, "_initialized"):
            self._initialized = True

        try:
            self._dbm = DatabaseManager()
        except psycopg2.Error:
            log.exception("Unable to initiate DatabaseManager.")

    async def find(self, name: str, lang: str, extended=False) -> Optional[Fact]:
        find_query = sql.SQL("SELECT * FROM fact WHERE name = %s AND lang = %s")
        extended_query = sql.SQL('SELECT last_edit, last_editor from fact_detail '
                                 'WHERE fact_name = %s AND fact_lang = %s')
        query_result = await self._dbm.query(find_query, (name.lower(), lang.lower()))

        if not query_result:
            return None

        return Fact(*query_result[0])

    async def update(self, name: str, lang: str, author: str, content: str):
        pass

    async def add(self, name: str, lang: str, author: str, content: str):
        pass

    async def mfd(self, name: str, lang: str, value: bool, author: str):
        pass

    async def remove(self, name: str, lang: str, author: str):
        """
        Removes a fact from the database.  NYI.
        Args:
            name: Name of fact
            lang: language ID of fact
            author: Person authoring and authorizing change

        Returns:
                (NYI) bool True on Success.
        """
        return NotImplementedError

    async def _details(self, value:Fact):
        pass

    async def _find(self, name: str, lang: str):
        pass

