from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NewForm
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NewForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data.capitalize()).first()
        if user is None:
            user = User(username=form.name.data.capitalize())
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        # this helps set the name field in form to be reset to none when POST request completes.
        session['name'] = form.name.data
        form.name.data = ''
        # if you do not have redirect then the POST request saves the data and when page, refreshes it gives you an
        # error of blank form submission.
        return redirect(url_for('.index'))
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False))