"""
facts_manager.py - Manages fact storage and retrieval.

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md

This module is built on top of the Pydle system.
"""


import logging
from facts.database_manager import DatabaseManager
from utils.ratlib import Singleton

log = logging.getLogger(f"mecha.{__name__}")


class FactManager(Singleton):

    # Define our safe tables for FM
    def safe_tables(self):
        return ["fact", "fact_timestamp"]

    def __init__(self):

        # Set our tables for safe_tables

        self.DatabaseManager = DatabaseManager()

