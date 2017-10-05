# -*- coding: utf-8 -*-
"""Permission model."""

from __future__ import absolute_import, division, print_function, unicode_literals

import datetime as dt

from ..database import Column, Model, SurrogatePK, db, reference_col, relationship


class Permission(SurrogatePK, Model):
    """A permission on a Collection, granted to a User."""

    __table_args__ = (db.UniqueConstraint('user_id', 'collection_id'), SurrogatePK.__table_args__)

    __tablename__ = 'permissions'
    user_id = reference_col('users', nullable=False)
    user = relationship('User', back_populates='permissions', uselist=False)

    collection_id = reference_col('collections', nullable=False)
    collection = relationship('Collection', back_populates='permissions', uselist=False)

    register = Column(db.Boolean(), default=False, nullable=False)
    catalogue = Column(db.Boolean(), default=False, nullable=False)

    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, user=None, collection=None, register=False, catalogue=False, **kwargs):
        """Create instance."""
        db.Model.__init__(self, user=user, collection=collection, register=register,
                          catalogue=catalogue, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Permission({user!r}@{collection!r})>'.format(user=self.user,
                                                              collection=self.collection)