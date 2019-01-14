"""
fact_cache.py - Fact Cache

Offline Fact cache.  Most used facts will be available if the database is not available.

Copyright (c) 2018 The Fuel Rat Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md
"""
import asyncio
import collections
import logging
from config import config
from Modules.fact_manager import Fact
from typing import Dict

log = logging.getLogger(f"mecha.{__name__}")


class FactCache(collections.MutableMapping):
    """
    Stores Facts in a cache (dict) to reduce required database lookups, and provides
    offline functionality to the Fact Manager.

    Facts are stored in a nested dictionary format:
    _cache = {
        "prep": {
            "en": "Please drop from supercruise and come to a....",
            "ru": "Cбросьте скорость до 30км/c, выйдите из..."
        },
        "kgbfoam": {
            "en": "To learn about Filtering the Galaxy Map...",
            "it": "Come filtrare la Mappa della Galassia..."
        }
    }
    """

    def _ttl_task(self):
        if self._offline:
            log.info("Fact Cache Maintenance did not run. Database is offline.")
            return

        del_count = 0
        decrement_count = 0
        to_delete = []
        for item in self._cache.keys():
            for fact in self._cache[item].values():
                if fact.ttl <= 1:
                    to_delete.append((item, fact.lang))
                    del_count += 1
                else:
                    decrement_count += 1
                    fact.ttl -= 1

        # Perform Deletions
        for key, subkey in to_delete:
            if to_delete:
                self._count -= 1
                del self._cache[key][subkey]

        log.info(f"FC Task Completed. {del_count} removed, {decrement_count} lowered.")
        log.info(f"[{self._count}] facts in cache.")

    async def _maintenance(self, interval: int):
        while self._offline is False:
            await asyncio.sleep(interval)
            await self._ttl_task()

    def __init__(self):
        self._cache = {}  # The actual cache is private
        self._count = 0  # Number of Facts contained within
        self._interval = config['caching'].get('interval') or 1800  # Default 1800 (30 min)
        self._ttl = config['caching'].get('ttl') or 12  # Default 12 (24 hours)
        self._offline = False  # Flag for offline mode.  Halts removal of expired facts.
        self._expiry_task = None

    def __getitem__(self, key: str) -> Dict[str, Fact]:
        if not isinstance(key, str):
            return NotImplemented
        return self._cache[key]

    def __setitem__(self, key, value: Fact):
        value.cached = True
        value.ttl = 12

        if key in self._cache:
            self._cache[key].update({value.lang: value})
        else:
            self._cache[key] = {value.lang: value}

        # Increase Counter
        self._count += 1

    def __delitem__(self, key):
        if not isinstance(key, str):
            return NotImplemented
        del self._cache[key]

        # Decrement counter
        self._count -= 1

    def __iter__(self):
        return iter(self._cache)

    def __len__(self):
        return self._count

    def __del__(self):
        if self._expiry_task:
            self._expiry_task.cancel()

    def __contains__(self, fact: Fact):
        if not isinstance(fact, Fact):
            return NotImplemented

        if fact.name not in self._cache:
            return False
        if fact.lang not in self._cache.values():
            return False
        else:
            return True










