from flask import Flask, make_response, abort, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def hello():
    response = make_response('<h1>This is a cookie inside a document</h1>')
    response.set_cookie('testcookie', '40')
    name = ['raj', 'test', 'test2', 'test3']
    return render_template('index.html', names=name)


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
