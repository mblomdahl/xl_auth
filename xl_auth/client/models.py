# -*- coding: utf-8 -*-
"""Client models."""

from __future__ import absolute_import, division, print_function, unicode_literals

from codecs import getencoder
from os import urandom

from six import string_types
from sqlalchemy.ext.hybrid import hybrid_property

from ..database import Column, Model, SurrogatePK, db


class Client(SurrogatePK, Model):
    """An OAuth2 Client."""

    __tablename__ = 'clients'
    client_id = Column(db.String(64), unique=True, nullable=False)
    client_secret = Column(db.String(256), unique=True, nullable=False)

    created_by = Column(db.ForeignKey('users.id'), nullable=False)

    is_confidential = Column(db.Boolean(), default=True, nullable=False)

    _redirect_uris = Column(db.Text(), nullable=False)
    _default_scopes = Column(db.Text(), nullable=False)

    # Human readable info fields
    name = Column(db.String(64))
    description = Column(db.String(400))

    def __init__(self, redirect_uris=None, default_scopes=None, **kwargs):
        """Create instance."""
        client_id = Client._generate_client_id()
        client_secret = Client._generate_client_secret()
        db.Model.__init__(self, client_id=client_id, client_secret=client_secret, **kwargs)
        self.redirect_uris = redirect_uris
        self.default_scopes = default_scopes

    @staticmethod
    def _generate_client_id():
        return getencoder('hex')(urandom(64))[0].decode('utf-8')[:8]

    @staticmethod
    def _generate_client_secret():
        return getencoder('hex')(urandom(256))[0].decode('utf-8')[:16]

    @hybrid_property
    def client_type(self):
        """Return client type."""
        if self.is_confidential:
            return 'confidential'
        else:
            return 'public'

    @hybrid_property
    def redirect_uris(self):
        """Return redirect URIs list."""
        return self._redirect_uris.split(' ')

    @redirect_uris.setter
    def redirect_uris(self, value):
        """Store redirect URIs list as string."""
        if isinstance(value, string_types):
            self._redirect_uris = value
        elif isinstance(value, list):
            self._redirect_uris = ' '.join(value)
        else:
            self._redirect_uris = value

    @hybrid_property
    def default_redirect_uri(self):
        """Return default redirect URI."""
        return self.redirect_uris[0]

    @hybrid_property
    def default_scopes(self):
        """Return default scopes list."""
        return self._default_scopes.split(' ')

    @default_scopes.setter
    def default_scopes(self, value):
        """Store default scopes list as string."""
        if isinstance(value, string_types):
            self._default_scopes = value
        elif isinstance(value, list):
            self._default_scopes = ' '.join(value)
        else:
            self._default_scopes = value

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Client({name!r})>'.format(name=self.name)
