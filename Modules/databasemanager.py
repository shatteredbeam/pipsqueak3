"""
database_manager.py - Manages access to the central database file

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md

This module is built on top of the Pydle system.
"""

from config import config
from psycopg2 import sql
from utils.ratlib import Singleton
import logging
import psycopg2

log = logging.getLogger(f"mecha.{__name__}")


class DatabaseManager(Singleton):

    # TODO: Abstraction
    # TODO: Getters/Setters
    # TODO: public/private properties/methods

    def __init__(self, *args, **kwargs):

        if not hasattr(self, "_initialized"):
            self._initialized = True
            self._connection = None
            self._connectionString = ''
            self._cursor = None
            self._dbhost = config['database']['host']
            self._dbport = config['database']['port']
            self._dbname = config['database']['dbname']
            self._dbuser = config['database']['username']
            self._dbpass = config['database']['password']
            self._retryattempts = config['database']['retry_attempts']
            self._retryinterval = config['database']['retry_interval']

    def _validateconnection(self):
        # Validate Connection Information
        if not self._dbhost:
            raise ValueError("Please set a database hostname [locahost/127.0.0.1]")
        if not self._dbport or not self._dbport.isdigit():
            log.debug("Bad or non-numeric database port. Defaulting to 5432.")
            self._dbport = 5432
        if not self._dbname:
            raise ValueError("Please set a database name. [mecha3]")
        if not self._dbuser:
            raise ValueError("Please set a database username.")
        if not self._dbpass:
            raise ValueError("Please set a database user password.")

        # Validate Retry Settings/Sanity
        if not self._retryinterval.isdigit():
            raise ValueError("Retry Interval must be an integer.")

        if not self._retryattempts.isdigit():
            raise ValueError("Retry Attempts must be an integer.")

        if self._retryinterval < 0 or self._retryinterval > 999:
            raise ValueError("Retry Interval must be between zero and 999 seconds.")

        if self._retryattempts < 0 or self._retryattempts > 100:
            raise ValueError("Retry Attempts must be between zero and 100.")

    def _buildconnectionstring(self):
        self._connectionString = f"host='{self._dbhost}', port='{self._dbport}', dbname='{self._dbname}', " \
                                 f"user='{self._dbuser}', password='{self._dbpass}'"

    async def _connect(self):
        # Build Connection String...
        self._buildconnectionstring()

        # Attempt to connect to the database, catching any errors in the process.
        try:
            self._connection = psycopg2.connect(self._connectionString)
        except psycopg2.Error as psyError:
            log.error(psyError)
        # Set Parameters of the connection(self)
        self._connection.set_session(autocommit=True)
        self._connection.set_client_encoding('utf-8')
        # Create main cursor
        self._cursor = self._connection.cursor()

    async def _query(self, query: sql.SQL):
        # Requires a composed sql.SQL string (should be passed from derived class) to prevent injection.
        if not isinstance(query, sql.SQL):
            raise TypeError("Expected composed SQL Object.")

        # Now that we can't pass a string, only a SQL object, the driver handles injection checking
        await self._cursor.execute(query)
