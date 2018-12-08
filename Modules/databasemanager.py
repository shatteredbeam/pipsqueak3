"""
database_manager.py - Manages access to the central database file

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md

This module is built on top of the Pydle system.
"""

from abc import abstractmethod
from config import config
from psycopg2 import sql
from utils.ratlib import Singleton
import logging
import psycopg2

log = logging.getLogger(f"mecha.{__name__}")


class Error(Exception):
    # Base Exception for DBM Errors
    pass


class TableScopeError(Error):
    # Raised by the DatabaseManager if a requested table is outside defined table scope.
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class DatabaseManager(Singleton):

    # TODO: Abstraction
    # TODO: Getters/Setters
    # TODO: public/private properties/methods

    @abstractmethod
    def safe_tables(self):
        pass

    def __init__(self,
                 dbhost=None,
                 dbPort=None,
                 dbName=None,
                 dbUser=None,
                 dbPassword=None,
                 safe_tables: list=None
                 ):

        # Singleton Check
        if not hasattr(self, "_initialized"):
            self._initialized = True

            # Set Instance properties
            self._connection = None
            self._cursor = None

            self._dbhost = config['database'].get('host')
            assert self._dbhost

            self._dbport = config['database'].get('port')
            assert self._dbport and self._dbport.isdecimal()

            self._dbname = config['database'].get('dbname')
            assert self._dbname

            self._dbuser = config['database'].get('username')
            assert self._dbuser

            self._dbpass = config['database'].get('password')
            assert self._dbpass

            self.__safe_tables = []

            self._connectionString = f"host='{self._dbhost}'," \
                f"port='{self._dbport}'," \
                f"dbname='{self._dbname}', " \
                f"user='{self._dbuser},'" \
                f"password='{self._dbpass}'," \
                f"'connect_timeout=5"

    async def _connect(self):
        # Attempt to connect to the database, catching any errors in the process.
        try:
            self._connection = await psycopg2.connect(self._connectionString)
        except psycopg2.Error as psyError:
            log.error(psyError)
        # Set Parameters of the connection(self)
        self._connection.set_session(autocommit=True)
        self._connection.set_client_encoding('utf-8')
        # Create main cursor
        self._cursor = self._connection.cursor()

    async def _query(self, query: sql.SQL) -> list:
        # Check the status of the connection before proceeding:
        if self._connection.status > 0:
            raise psycopg2.DatabaseError("Connection status is invalid for transaction.")

        # Requires a composed sql.SQL string (should be passed from derived class) to prevent injection.
        if not isinstance(query, sql.SQL):
            log.warning(f"Discarded Query (Type not SQL): [{self._cursor.mogrify(query)}]")
            raise TypeError("Expected composed SQL Object.")

        # Check that the table name is indeed in the sql query.  In this way, we force the whitelist validation
        # AND disallow attempts at global queries.
        if not any(table for table in self._cursor.mogrify(query) in self.__safe_tables):
            log.warning(f"Discarded Query (Table out of scope): [{self._cursor.mogrify(query)}]")
            raise TableScopeError(f"Requested Table out of scope. Available tables: {self.__safe_tables}")

        # Now that we can't pass a string, only a SQL object, the driver handles injection checking.  Use a
        # block here so psycopg2 will roll back a transaction that fails.
        try:
            self._cursor.execute(query)
            log.info(f"Accepted Query [{self._cursor.mogrify(query)}]")
        except psycopg2.Error as pgE:
            # Close the connection and re-establish.
            await self._cursor.close()
            await self._connection.close()

            # Clean up
            self._cursor = None
            self._connection = None

            # Attempt to Reconnect
            await self._connect()

            # Log the issue:
            log.error(f"Connection aborted and reconnecting: {pgE}")

        # Warning: May return an empty list.
        return list(await self._cursor.fetchall())

