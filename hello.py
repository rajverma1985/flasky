from flask import Flask, make_response, abort, render_template
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


@app.route('/')
def hello():
    response = make_response('<h1>This is a cookie inside a document</h1>')
    response.set_cookie('testcookie', '40')
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/username/<name>')
def user(name):
    if not user:
        abort(404)
    return render_template('index.html', name=name)


@app.route('/test')
def test():
    abort(500)
    return render_template('user.html')


# custom error pages

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 400


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
