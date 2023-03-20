from flask import Flask, make_response

app = Flask(__name__)


@app.route('/')
def hello():
    response = make_response('<h1>This is a cookie inside a document</h1>')
    response.set_cookie('testcookie', '40')
    return response


@app.route('/username/<user>')
def user(user):
    return f'<h1>Hello {user}</h1>'


if __name__ == "__main__":
    app.run(port=5000)
