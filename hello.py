from flask import Flask, make_response, abort, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    response = make_response('<h1>This is a cookie inside a document</h1>')
    response.set_cookie('testcookie', '40')
    return render_template('index.html')


@app.route('/username/<name>')
def user(name):
    if not user:
        abort(404)
    return render_template('index.html', name=name)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
