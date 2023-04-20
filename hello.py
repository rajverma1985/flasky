from flask import Flask, abort, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config["SECRET_KEY"] = "some_random_key_here"


# Creating a form object from Flaskform class

class NewForm(FlaskForm):
    name = StringField('What is your Name', validators=[DataRequired()])
    submit = SubmitField('Submit Form')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NewForm()
    if form.validate_on_submit():
        saved_name = session.get('name')
        if saved_name is not None and saved_name != form.name.data:
            flash("You seem to have changed your name")
        session['name'] = form.name.data
        # this helps set the name field in form to be reset to none when POST request completes.
        # form.name.data = ''
        # if you do not have redirect then the POST request saves the data and when page
        # refreshes it gives you an error of blank form submission.
        return redirect(url_for('index'))
    return render_template('index.html',
                           current_time=datetime.utcnow(), form=form,
                           name=session.get('name'))


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


if __name__ == "__main__":
    app.run(port=5000, debug=True)
