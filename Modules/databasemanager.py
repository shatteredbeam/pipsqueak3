"""
database_manager.py - Manages access to the central database file

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md

This module is built on top of the Pydle system.
"""

from config import config
from typing import Optional
from utils.ratlib import Singleton
import datetime
import logging
import pyodbc

log = logging.getLogger(f"mecha.{__name__}")


class DatabaseManager(Singleton):

    _QUERY_CREATE_FACT_TABLE = "CREATE TABLE IF NOT EXISTS ", \
                               "fact (name VARCHAR NOT NULL,lang "\
                               "VARCHAR NOT NULL,message VARCHAR NOT NULL, ",\
                               "author VARCHAR, PRIMARY KEY (name, lang));"

    _QUERY_CREATE_TIMESTAMP_TABLE = "CREATE TABLE IF NOT EXISTS fact_timestamps ",\
                                    "(id SERIAL PRIMARY KEY, name VARCHAR NOT NULL, ",\
                                    "lang VARCHAR NOT NULL, message VARCHAR NOT NULL, ", \
                                    "author VARCHAR NOT NULL, date_changed ", \
                                    "TIMESTAMP WITH TIME ZONE NOT NULL);"

    _ERROR_SUFFIX = "This is required with the chosen connection type."

    # TODO: Abstraction
    # TODO: Getters/Setters
    # TODO: public/private properties/methods

    def __init__(self, *args, **kwargs):

        if not hasattr(self, "_initialized"):
            self._initialized = True
            self._connection: Optional[pyodbc.Connection] = None
            self._cursor: Optional[pyodbc.Cursor] = None
            self._connectionString = config['database']['odbc_string']
            self._connectionType = config['database']['connection_type']
            self._dsn = config['database']['dsn']
            self._dsnuid = config['database']['dsn_uid']
            self._dsnpwd = config['database']['dsn_pwd']
            self._retryattempts = config['database']['retry_attempts']
            self._retryinterval = config['database']['retry_interval']

    def _validateconnection(self):
        # Validate Connection Type
        if self._connectionType.casefold() not in ["odbc", "dsn"]:
            raise ValueError("Invalid Connection Type. " + self._ERROR_SUFFIX)

        # Validate ODBC Settings
        if not self._connectionString:
            raise ValueError("No ODBC String entered. " + self._ERROR_SUFFIX)

        # Validate DSN Settings
        if self._connectionType.casefold() == 'dsn':
            if self._dsn:
                raise ValueError("No DSN Entered. " + self._ERROR_SUFFIX)
            if not self._dsnuid:
                raise ValueError("No DSN UID Entered. " + self._ERROR_SUFFIX)
            if not self._dsnpwd:
                raise ValueError("No DSN Password Entered." + self._ERROR_SUFFIX)

        # Validate Retry Settings(Both must be an integer)
        if not self._retryinterval.isdigit():
            raise ValueError("Retry Interval must be an integer.")

        if not self._retryattempts.isdigit():
            raise ValueError("Retry Attempts must be an integer.")

        if self._retryinterval < 0 or self._retryinterval > 999:
            raise ValueError("Retry Interval must be between zero and 999 seconds.")

        if self._retryattempts < 0 or self._retryattempts > 100:
            raise ValueError("Retry Attempts must be between zero and 100.")

    def _connect(self):
        try:
            self._connection = pyodbc.connect(self._connectionString)
        except (pyodbc.Error, pyodbc.ProgrammingError) as pyodbcError:
            log.error(pyodbcError)

        # Set Parameters of the connection(self)
        self._connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        self._connection.setencoding(pyodbc.SQL_CHAR, encoding='utf-8')
        self._connection.maxwrite = 1024 * 1024 * 1024

        # Create main cursor
        self._cursor = self._connection.cursor()

        # Check if the database has been initialized with the tables we need:

    async def _verifytablestructure(self):
        try:
            self._cursor.execute("SELECT 1 FROM fact")
            tablecheck = self._cursor.commit()

            self._cursor.execute("SELECT 1 FROM fact_timestamps")
            tscheck = self._cursor.commit()

            if not tablecheck:
                log.warning("Facts Table does not exist or is inaccessible.")
            if not tscheck:
                log.warning("Fact Timestamp Table does not exist or is inaccessible")

        except pyodbc.DatabaseError as pyodbcError:
            log.error(pyodbcError)

        finally:
            if self._connection:
                self._connection.close()


















