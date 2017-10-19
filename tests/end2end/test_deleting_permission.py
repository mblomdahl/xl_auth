# -*- coding: utf-8 -*-
"""Test deleting permissions."""

from __future__ import absolute_import, division, print_function, unicode_literals

from flask_babel import gettext as _

from xl_auth.permission.models import Permission


# noinspection PyUnusedLocal
def test_superuser_can_delete_existing_permission(superuser, permission, testapp):
    """Delete existing permission."""
    old_count = len(Permission.query.all())
    # Goes to homepage
    res = testapp.get('/')
    # Fills out login form
    form = res.forms['loginForm']
    form['username'] = superuser.email
    form['password'] = 'myPrecious'
    # Submits
    res = form.submit().follow()
    # Clicks Permissions button
    res = res.click(_('Permissions'))
    # Clicks Edit button on a permission
    res = res.click(_('Edit'))
    # Clicks Delete button on a permission
    permission_user_email = permission.user.email
    permission_collection_code = permission.collection.code
    res = res.click(_('Delete Permission')).follow()
    assert res.status_code == 200
    # Permission was deleted, so number of permissions are 1 less than initial state
    assert _('Successfully deleted permissions for "%(username)s" on collection "%(code)s".',
             username=permission_user_email, code=permission_collection_code) in res
    assert len(Permission.query.all()) == old_count - 1


def test_user_cannot_delete_permission(user, permission, testapp):
    """Attempt to delete a permission."""
    old_count = len(Permission.query.all())
    # Goes to homepage
    res = testapp.get('/')
    # Fills out login form
    form = res.forms['loginForm']
    form['username'] = user.email
    form['password'] = 'myPrecious'
    # Submits
    res = form.submit().follow()

    # We see no Permissions button
    assert res.lxml.xpath("//a[contains(@text,'{0}')]".format(_('Permissions'))) == []

    # Try to go there directly
    testapp.get('/permissions/', status=403)

    # Try to delete
    testapp.delete('/permissions/delete/1', status=403)

    # Nothing was deleted
    assert len(Permission.query.all()) == old_count
