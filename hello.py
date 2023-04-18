from flask import Flask, make_response, abort, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap =Bootstrap(app)


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
    return render_template('user.html')
if __name__ == "__main__":
    app.run(port=5000, debug=True)
