# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""

from __future__ import absolute_import, division, print_function, unicode_literals

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user, login_required, login_user, logout_user

from six.moves.urllib_parse import quote

from ..extensions import login_manager
from ..public.forms import LoginForm
from ..user.models import User
from ..utils import flash_errors

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@login_manager.unauthorized_handler
def redirect_unauthorized():
    """Redirect to login screen."""
    return redirect(url_for('public.home') + '?next={}'.format(quote(request.full_path)))


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    login_form = LoginForm(request.form)
    # Handle logging in.
    if request.method == 'POST':
        if login_form.validate_on_submit():
            login_user(login_form.user)
            flash(_('You are logged in.'), 'success')
            redirect_url = login_form.next_redirect.data or url_for('user.profile')
            current_user.update_last_login()
            return redirect(redirect_url)
        else:
            flash_errors(login_form)
    return render_template('public/home.html', login_form=login_form,
                           next_redirect_url=request.args.get('next'))


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash(_('You are logged out.'), 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/about/')
def about():
    """About page."""
    return render_template('public/about.html', version=current_app.config['APP_VERSION'])
