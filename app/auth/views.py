from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from ..email import send_email
from ..models import User, db
from .forms import LoginForm, RegisterForm, ChangePassword


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm_token(token):
        db.session.commit()  # This sends a commit for confirmed column to the database as per the user model
        flash("Thanks for confirming you email")
    else:
        flash("The confirmation link has expired or invalid.")
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    return redirect(url_for('main.index'))


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
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', register_form=reg_form)


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_passwords():
    form = ChangePassword()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash("Your password is updated")
            return redirect(url_for('main.index'))
        else:
            flash("Wrong Old Password, Please check you password and try again!")
    return render_template('auth/change_password.html', form=form)
