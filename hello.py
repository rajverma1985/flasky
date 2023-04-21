from flask import Flask, abort, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config["SECRET_KEY"] = "some_random_key_here"
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://raj:test@localhost/flasky"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# model definition

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # user refers to the instance of the class Role
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return "<Role %r>" % self.name


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # this is the foreign key colum for users table which refers to roles tables id column
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return "<User %r>" % self.username


# Creating a form object from Flaskform class

class NewForm(FlaskForm):
    name = StringField('What is your Name', validators=[DataRequired()])
    submit = SubmitField('Submit Form')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NewForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data.first())
        # saved_name = session.get('name')
        # if saved_name is not None and saved_name != form.name.data:
        #     flash("You seem to have changed your name")
        if user is None:
            session['known'] = False
            db.session.add(user)
            db.session.commit()
        else:
            session['known'] = True
            user = form.name.data
            # this helps set the name field in form to be reset to none when POST request completes.
            form.name.data = ''
        # if you do not have redirect then the POST request saves the data and when page, refreshes it gives you an error of blank form submission.
        return redirect(url_for('index'))
    print(session.keys(), session.values())
    return render_template('index.html',
                           current_time=datetime.utcnow(), form=form,
                           name=session.get('name'), known=session.get('known', False))


@app.route('/username/<name>')
def user(name):
    if not user:
        abort(404)
    return render_template('index.html', name=name)


# custom error pages

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 400


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# creating some roles and users

# admin = Role(name="Admin")
# Moderator = Role(name="Moderator")
# normal_user = Role(name="Normal_user")
# user1 = User(username='user1', role=admin)
# user2 = User(username='user2', role=Moderator)
# user3 = User(username='user3', role=normal_user)
# user4 = User(username='user4', role=normal_user)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
