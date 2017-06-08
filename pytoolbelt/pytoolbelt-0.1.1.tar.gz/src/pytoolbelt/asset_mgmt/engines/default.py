# -*- coding: utf-8 -*-

# This module is part of onfo_octavius and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
#
# this enine is used by the onfo_ocatvius asset management module
# it describes, how a filestream will be saved to the filesystem
# and registered/referenced in a database
#

import logging, collections, sqlalchemy, datetime, transaction

import sqlalchemy.ext.declarative as sqla_decl
import sqlalchemy.orm as sqla_orm
from zope.sqlalchemy import ZopeTransactionExtension

import pytoolbelt.asset_mgmt.handler as core_handler

Base = sqla_decl.declarative_base()


log = logging.getLogger(__name__)

# The Ident-object provides the required information for determining 
# a unique, file-specific naming
Ident = collections.namedtuple("Ident", ("id", "parent_id", "str1",))
Credentials = collections.namedtuple("Credentials", ("storage_directory", "alchemy_session",))

def resolve_filepath(id, mime_type):
    id = id
    top_dir = "%02x" % (0xff & (id >> 8),)
    sub_dir = "%02x" % (0xff & (id >> 16),)
    file = "%012x%s" % ((0xff & id) | (id >> 24), core_handler.extension(mime_type))
    return "/".join((top_dir, sub_dir, file,))


class FileInfo(core_handler.FileInfo):
    """ FileInfo-Implementation for the DefaultStorageEngine
    
    all required file-infos will be provided by a sqlalchemy-dao
    and the engine-credentials 
    """
    def __init__(self, data, storage_directory):
        self._data = data
        self._storage_directory = storage_directory

        self.ident = Ident(data.id, data.parent_id, data.str1)
        self.original_filename = data.original_filename
        self.mime_type = data.mime_type

        self.path_to_file = resolve_filepath(data.id, data.mime_type)
        
        self.full_path_to_file = "/".join((self._storage_directory,self.path_to_file,))


class Asset(Base):
    __tablename__ = 'asset'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    original_filename = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    mime_type = sqlalchemy.Column(sqlalchemy.VARCHAR(10), nullable=False)
    int1 = sqlalchemy.Column(sqlalchemy.INTEGER(2), nullable=True)
    str1 = sqlalchemy.Column(sqlalchemy.VARCHAR(100), nullable=True)
    created_on = sqlalchemy.Column(sqlalchemy.DATETIME, nullable=False, default=datetime.datetime.utcnow)
    modified_on = sqlalchemy.Column(sqlalchemy.DATETIME, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, original_filename, mime_type):
        self.original_filename = original_filename
        self.mime_type = mime_type

    def __repr__(self):
        return u"Asset(id=%s, parent_id=%s, str1=%s, mime_type=%s, )" % (self.id, self.parent_id, self.str1, self.mime_type)


class DefaultStorageEngine(object):
    def __init__(self, credentials):
        self.storage_directory = credentials.storage_directory
        self.alchemy_session = credentials.alchemy_session

    def store(self, stream, filename, mime_type, ident=Ident(None, None, None), str1=None, int1=None):
        log.info(u"register a asset to the database (filename=%s, mime_type=%s, ident=%s)" % (filename, mime_type, ident))
        data = Asset(filename, mime_type)
        
        if not str1 is None: data.str1 = str1
        if not int1 is None: data.int1 = int1
        
        with transaction.manager:
            self.alchemy_session.add(data)
        
        # TODO: save the file to the filesystem
        
        return FileInfo(data, self.storage_directory)

    def load(self, ident):
        data = None
        
        if ident.id is None:
            raise ValueError(u"ID-value can not be None (data=%s)"  % ident.id)
        
        with transaction.manager:
            query = self.alchemy_session.query(Asset)
            query = query.filter(Asset.id==ident.id)
            
            if query.count() == 1:
                return FileInfo(query.first(), self.storage_directory)
            
            log.info(u"no matching record could be found for the given ident (ident=%s)" % ident)
        
        return None
