# -*- coding: utf-8 -*-
"""Report models."""
import json
from cached_property import cached_property

from .extensions import db

# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class."""

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
                (isinstance(record_id, (str, bytes)) and record_id.isdigit(),
                 isinstance(record_id, (int, float))),
        ):
            return cls.query.get(int(record_id))
        return None


class Report(SurrogatePK, db.Model):
    """A report."""

    __tablename__ = 'reports'

    type = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Report({id})>'.format(id=self.id)

    @cached_property
    def type_dict(self):
        return json.loads(self.type)
