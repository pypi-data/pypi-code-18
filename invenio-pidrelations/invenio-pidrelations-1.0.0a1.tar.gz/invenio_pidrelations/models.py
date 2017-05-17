# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2014, 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Persistent identifier's relations models."""

from __future__ import absolute_import, print_function

import logging

from flask_babelex import gettext
from invenio_db import db
from invenio_pidstore.models import PersistentIdentifier
from speaklater import make_lazy_gettext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import backref
from sqlalchemy_utils.models import Timestamp

_ = make_lazy_gettext(lambda: gettext)

logger = logging.getLogger('invenio-pidrelations')


class PIDRelation(db.Model, Timestamp):
    """Model persistent identifier relations."""

    __tablename__ = 'pidrelations_pidrelation'

    parent_id = db.Column(
        db.Integer,
        db.ForeignKey(PersistentIdentifier.id, onupdate="CASCADE",
                      ondelete="CASCADE",
                      name='fk_pidrelation_parent_pidstore_pid'),
        nullable=False,
        primary_key=True,
        )
    """Parent PID of the relation."""

    child_id = db.Column(
        db.Integer,
        db.ForeignKey(PersistentIdentifier.id, onupdate="CASCADE",
                      ondelete="CASCADE",
                      name='fk_pidrelation_parent_pidstore_pid'),
        nullable=False,
        primary_key=True)
    """Child PID of the relation."""

    relation_type = db.Column(
        db.SmallInteger(),
        nullable=False)
    """Type of relation between the parent and child PIDs."""

    index = db.Column(db.Integer, nullable=True)
    """Index of the PID relation (e.g.: modeling ordered sequence of PIDs)."""

    #
    # Relations
    #
    parent = db.relationship(
        PersistentIdentifier,
        primaryjoin=PersistentIdentifier.id == parent_id,
        backref=backref('child_relations', lazy='dynamic',
                        cascade='all,delete'))

    child = db.relationship(
        PersistentIdentifier,
        primaryjoin=PersistentIdentifier.id == child_id,
        backref=backref('parent_relations', lazy='dynamic',
                        cascade='all,delete'))

    def __repr__(self):
        """Text representation of a PID relation."""
        return "<PIDRelation: ({r.parent.pid_type}:{r.parent.pid_value}) -> " \
               "({r.child.pid_type}:{r.child.pid_value}) " \
               "(Type: {r.relation_type}, Idx: {r.index})>".format(r=self)

    @classmethod
    def get_parent_relations(cls, pid):
        """Get all relations where given PID is a parent."""
        return cls.query.filter((cls.parent == pid))

    @classmethod
    def get_child_relations(cls, pid):
        """Get all relations where given PID is a child."""
        return cls.query.filter((cls.child == pid))

    @classmethod
    def create(cls, parent, child, relation_type, index=None):
        """Create a PID relation for given parent and child."""
        try:
            with db.session.begin_nested():
                obj = cls(parent_id=parent.id,
                          child_id=child.id,
                          relation_type=relation_type,
                          index=index)
                db.session.add(obj)
        except IntegrityError:
            raise Exception("PID Relation already exists.")
            # msg = "PIDRelation already exists: " \
            #       "{0} -> {1} ({2})".format(
            #         parent_pid, child_pid, relation_type)
            # logger.exception(msg)
            # raise Exception(msg)
        return obj

    @classmethod
    def relation_exists(self, parent, child, relation_type):
        """Determine if given relation already exists."""
        return PIDRelation.query.filter_by(
            child_pid_id=child.id,
            parent_pid_id=parent.id,
            relation_type=relation_type).count() > 0


__all__ = (
    'PIDRelation',
)
