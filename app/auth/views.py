from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import auth
from ..models import User, db
from .forms import LoginForm, RegisterForm
from itsdangerous import URLSafeTimedSerializer as Serializer



@auth.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data).first()
        if user is not None and user.verify_password(loginform.password.data):
            login_user(user, loginform.remember_me.data)
            new = request.args.get('new')
            if new is None or not new.startswith('/'):
                new = url_for('main.index')
            return redirect(new)
        flash("Invalid username or password")
    return render_template('auth/login.html', loginform=loginform)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        user = User(email=reg_form.email.data,
                    username=reg_form.username.data,
                    password=reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Successfully Registered, you can login now!")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', register_form=reg_form)
