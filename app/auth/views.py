from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from ..email import send_email
from ..models import User, db
from .forms import LoginForm, RegisterForm


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.not_confirmed'))


@auth.route('/unconfirmed')
def not_confirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()  # This sends a commit for confirmed column to the database as per the user model
        flash("Thanks for confirming you email")
    else:
        flash("The confirmation link has expired or invalid.")
    return redirect(url_for('main.index'))


@auth.route('/resend_confirmation')
@login_required
def resend_confirmation():
    token = current_user.generate_token()
    send_email()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data.lower()).first()
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
        user = User(email=reg_form.email.data.lower(),
                    username=reg_form.username.data,
                    password=reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Successfully Registered, you can login now!")
        token = user.generate_token()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', register_form=reg_form)
