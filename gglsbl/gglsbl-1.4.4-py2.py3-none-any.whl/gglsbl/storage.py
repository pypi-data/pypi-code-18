#!/usr/bin/env python

import os
import hashlib
import contextlib
import sqlite3

import logging
log = logging.getLogger('gglsbl')
log.addHandler(logging.NullHandler())

from gglsbl.utils import to_hex

class ThreatList(object):
    """Represents threat list name.
    """
    def __init__(self, threat_type, platform_type, threat_entry_type):
        self.threat_type = threat_type
        self.platform_type = platform_type
        self.threat_entry_type = threat_entry_type

    @classmethod
    def from_api_entry(cls, entry):
        return cls(entry['threatType'], entry['platformType'], entry['threatEntryType'])

    def as_tuple(self):
        return (self.threat_type, self.platform_type, self.threat_entry_type)

    def __repr__(self):
        return '/'.join(self.as_tuple())


class HashPrefixList(object):
    """Wrapper object for threat list data.
    """
    def __init__(self, prefix_size, raw_hashes):
        self.prefix_size = prefix_size
        self.raw_hashes = raw_hashes

    def __len__(self):
        return int(len(self.raw_hashes) / self.prefix_size)

    def __iter__(self):
        n = self.prefix_size
        return (self.raw_hashes[i:i+n] for i in range(0, len(self.raw_hashes), n))


class SqliteStorage(object):
    """Storage abstraction for local GSB cache"""
    def __init__(self, db_path):
        self.db_path = db_path
        do_init_db = not os.path.isfile(db_path)
        log.info('Opening SQLite DB {}'.format(db_path))
        self.db = sqlite3.connect(db_path)
        if do_init_db:
            log.info('SQLite DB does not exist, initializing')
            self.init_db()
        self.db.cursor().execute('PRAGMA synchronous = 0')

    @contextlib.contextmanager
    def get_cursor(self):
        dbc = self.db.cursor()
        try:
            yield dbc
        finally:
            dbc.close()

    def init_db(self):
        with self.get_cursor() as dbc:
            dbc.execute(
            """CREATE TABLE threat_list (
                threat_type character varying(128) NOT NULL,
                platform_type character varying(128) NOT NULL,
                threat_entry_type character varying(128) NOT NULL,
                client_state character varying(42),
                timestamp timestamp without time zone DEFAULT current_timestamp,
                PRIMARY KEY (threat_type, platform_type, threat_entry_type)
                )"""
            )
            dbc.execute(
            """CREATE TABLE full_hash (
                value BLOB NOT NULL,
                threat_type character varying(128) NOT NULL,
                platform_type character varying(128) NOT NULL,
                threat_entry_type character varying(128) NOT NULL,
                downloaded_at timestamp without time zone DEFAULT current_timestamp,
                expires_at timestamp without time zone NOT NULL DEFAULT current_timestamp,
                malware_threat_type varchar(32),
                PRIMARY KEY (value, threat_type, platform_type, threat_entry_type)
                )"""
            )
            dbc.execute(
            """CREATE TABLE hash_prefix (
                value BLOB NOT NULL,
                cue character varying(4) NOT NULL,
                threat_type character varying(128) NOT NULL,
                platform_type character varying(128) NOT NULL,
                threat_entry_type character varying(128) NOT NULL,
                timestamp timestamp without time zone DEFAULT current_timestamp,
                negative_expires_at timestamp without time zone NOT NULL DEFAULT current_timestamp,
                PRIMARY KEY (value, threat_type, platform_type, threat_entry_type),
                FOREIGN KEY(threat_type, platform_type, threat_entry_type)
                    REFERENCES threat_list(threat_type, platform_type, threat_entry_type)
                    ON DELETE CASCADE
                )"""
            )
            dbc.execute(
                """CREATE INDEX idx_hash_prefix_cue ON hash_prefix (cue)"""
            )
            dbc.execute(
                """CREATE INDEX idx_full_hash_expires_at ON full_hash (expires_at)"""
            )
            dbc.execute(
                """CREATE INDEX idx_full_hash_value ON full_hash (value)"""
            )
        self.db.commit()

    def lookup_full_hashes(self, hash_values):
        "Query DB to see if hash is blacklisted"
        q = '''SELECT threat_type,platform_type,threat_entry_type, expires_at < current_timestamp AS has_expired
                FROM full_hash WHERE value IN ({})
        '''
        output = []
        with self.get_cursor() as dbc:
            dbc.execute(q.format(','.join(['?']*len(hash_values))), [sqlite3.Binary(hv) for hv in hash_values])
            for h in dbc.fetchall():
                threat_type, platform_type, threat_entry_type, has_expired = h
                threat_list = ThreatList(threat_type, platform_type, threat_entry_type)
                output.append((threat_list, has_expired))
        return output

    def lookup_hash_prefix(self, cues):
        """Lookup hash prefixes by cue (first 4 bytes of hash)

        Returns a tuple of (threat_list, value, negative_cache_expired).
        """
        q = '''SELECT value,threat_type,platform_type,threat_entry_type,
                    negative_expires_at < current_timestamp AS negative_cache_expired
                FROM hash_prefix WHERE cue IN ({})
        '''
        output = []
        with self.get_cursor() as dbc:
            dbc.execute(q.format(','.join(['?'] * len(cues))), cues)
            for h in dbc.fetchall():
                value, threat_type, platform_type, threat_entry_type, negative_cache_expired = h
                threat_list = ThreatList(threat_type, platform_type, threat_entry_type)
                output.append((threat_list, bytes(value), negative_cache_expired))
        return output

    def store_full_hash(self, threat_list, hash_value, cache_duration, malware_threat_type):
        "Store full hash found for the given hash prefix"

        log.info('Storing full hash {} to list {} with cache duration {}'.format(to_hex(hash_value), str(threat_list), cache_duration))
        qi = '''INSERT OR IGNORE INTO full_hash
                    (value, threat_type, platform_type, threat_entry_type, malware_threat_type, downloaded_at)
                VALUES
                    (?, ?, ?, ?, ?, current_timestamp)
        '''
        qu = "UPDATE full_hash SET expires_at=datetime(current_timestamp, '+{} SECONDS') \
            WHERE value=? AND threat_type=? AND platform_type=? AND threat_entry_type=?"

        i_parameters = [sqlite3.Binary(hash_value), threat_list.threat_type,
                    threat_list.platform_type, threat_list.threat_entry_type, malware_threat_type]
        u_parameters = [sqlite3.Binary(hash_value), threat_list.threat_type,
                    threat_list.platform_type, threat_list.threat_entry_type]

        with self.get_cursor() as dbc:
            dbc.execute(qi, i_parameters)
            dbc.execute(qu.format(int(cache_duration)), u_parameters)
        self.db.commit()

    def delete_hash_prefix_list(self, threat_list):
        q = '''DELETE FROM hash_prefix
                    WHERE threat_type=? AND platform_type=? AND threat_entry_type=?
        '''
        parameters = [threat_list.threat_type, threat_list.platform_type, threat_list.threat_entry_type]
        with self.get_cursor() as dbc:
            dbc.execute(q, parameters)
        self.db.commit()

    def cleanup_full_hashes(self, keep_expired_for=60*60*12):
        """Remove long expired full_hash entries.
        """
        q = '''DELETE FROM full_hash WHERE expires_at=datetime(current_timestamp, '{} SECONDS')
        '''
        log.info('Cleaning up full_hash entries expired more than {} seconds ago.'.format(keep_expired_for))
        with self.get_cursor() as dbc:
            dbc.execute(q.format(int(keep_expired_for)))
        self.db.commit()

    def update_hash_prefix_expiration(self, threat_list, prefix_value, negative_cache_duration):
        q = "UPDATE hash_prefix SET negative_expires_at=datetime(current_timestamp, '+{} SECONDS') \
            WHERE value=? AND threat_type=? AND platform_type=? AND threat_entry_type=?"
        parameters = [sqlite3.Binary(prefix_value), threat_list.threat_type,
                    threat_list.platform_type, threat_list.threat_entry_type]
        with self.get_cursor() as dbc:
            dbc.execute(q.format(int(negative_cache_duration)), parameters)
        self.db.commit()

    def get_threat_lists(self):
        """Get a list of known threat lists including clientState values.
        """
        q = '''SELECT threat_type,platform_type,threat_entry_type,client_state FROM threat_list'''
        output = []
        with self.get_cursor() as dbc:
            dbc.execute(q)
            for h in dbc.fetchall():
                threat_type, platform_type, threat_entry_type, client_state = h
                threat_list = ThreatList(threat_type, platform_type, threat_entry_type)
                output.append((threat_list, client_state))
        return output

    def add_threat_list(self, threat_list):
        """Add threat list entry if it does not exist.
        """
        q = '''INSERT OR IGNORE INTO threat_list
                    (threat_type, platform_type, threat_entry_type, timestamp)
                VALUES
                    (?, ?, ?, current_timestamp)
        '''
        params = [threat_list.threat_type, threat_list.platform_type, threat_list.threat_entry_type]
        with self.get_cursor() as dbc:
            dbc.execute(q, params)
        self.db.commit()

    def delete_threat_list(self, threat_list):
        """Delete threat list entry.
        """
        log.info('Deleting cached threat list "{}"'.format(repr(threat_list)))
        q = '''DELETE FROM threat_list
                    WHERE threat_type=? AND platform_type=? AND threat_entry_type=?
        '''
        params = [threat_list.threat_type, threat_list.platform_type, threat_list.threat_entry_type]
        with self.get_cursor() as dbc:
            dbc.execute(q, params)
        self.db.commit()

    def update_threat_list_client_state(self, threat_list, client_state):
        log.info('Setting client_state of threat list {} to {}'.format(str(threat_list), client_state))
        q = '''UPDATE threat_list SET timestamp=current_timestamp, client_state=?
            WHERE threat_type=? AND platform_type=? AND threat_entry_type=?'''
        params = [client_state, threat_list.threat_type, threat_list.platform_type, threat_list.threat_entry_type]
        with self.get_cursor() as dbc:
            dbc.execute(q, params)
        self.db.commit()

    def hash_prefix_list_checksum(self, threat_list):
        """Returns SHA256 checksum for alphabetically-sorted concatenated list of hash prefixes
        """
        q = '''SELECT value FROM hash_prefix
                WHERE threat_type=? AND platform_type=? AND threat_entry_type=?
                ORDER BY value
        '''
        params = [threat_list.threat_type, threat_list.platform_type, threat_list.threat_entry_type]
        with self.get_cursor() as dbc:
            dbc.execute(q, params)
            all_hashes = b''.join([ bytes(h[0]) for h in dbc.fetchall() ])
            checksum = hashlib.sha256(all_hashes).digest()
        return checksum

    def populate_hash_prefix_list(self, threat_list, hash_prefix_list):
        log.info('Storing {} entries of hash prefix list {}'.format(len(hash_prefix_list), str(threat_list)))
        q = '''INSERT INTO hash_prefix
                    (value, cue, threat_type, platform_type, threat_entry_type, timestamp)
                VALUES
                    (?, ?, ?, ?, ?, current_timestamp)
        '''
        with self.get_cursor() as dbc:
            records = [[sqlite3.Binary(prefix_value), to_hex(prefix_value[0:4]), threat_list.threat_type,
                        threat_list.platform_type, threat_list.threat_entry_type] for prefix_value in hash_prefix_list]
            dbc.executemany(q, records)
        #self.db.commit()

    def get_hash_prefix_values_to_remove(self, threat_list, indices):
        log.info('Removing {} records from threat list "{}"'.format(len(indices), str(threat_list)))
        indices = set(indices)
        q = '''SELECT value FROM hash_prefix
                WHERE threat_type=? AND platform_type=? AND threat_entry_type=?
                ORDER BY value
        '''
        params = [threat_list.threat_type, threat_list.platform_type, threat_list.threat_entry_type]
        values_to_remove = []
        with self.get_cursor() as dbc:
            dbc.execute(q, params)
            i = 0
            for h in dbc.fetchall():
                v = bytes(h[0])
                if i in indices:
                    values_to_remove.append(v)
                i += 1
        return values_to_remove

    def remove_hash_prefix_indices(self, threat_list, indices):
        """Remove records matching idices from a lexicographically-sorted local threat list.
        """
        batch_size = 40
        q = '''DELETE FROM hash_prefix
                WHERE threat_type=? AND platform_type=? AND threat_entry_type=? AND value IN ({})
        '''
        prefixes_to_remove = self.get_hash_prefix_values_to_remove(threat_list, indices)
        with self.get_cursor() as dbc:
            for i in range(0, len(prefixes_to_remove), batch_size):
                remove_batch = prefixes_to_remove[i:(i+batch_size)]
                params = [threat_list.threat_type, threat_list.platform_type, threat_list.threat_entry_type] + \
                                [sqlite3.Binary(b) for b in remove_batch]
                dbc.execute(q.format(','.join(['?'] * len(remove_batch))), params)

    def total_cleanup(self):
        "Reset local cache"
        with self.get_cursor() as dbc:
            q = 'DROP TABLE threat_list'
            dbc.execute(q)
            q = 'DROP TABLE hash_prefix'
            dbc.execute(q)
            q = 'DROP TABLE full_prefix'
            dbc.execute(q)
        self.db.commit()
        self.init_db()
