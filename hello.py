from flask import Flask, make_response, abort

app = Flask(__name__)


@app.route('/')
def hello():
    response = make_response('<h1>This is a cookie inside a document</h1>')
    response.set_cookie('testcookie', '40')
    return response


@app.route('/username/<id>')
def user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello {}, your id is {}</h1>'.format(user.name, user.id)


if __name__ == "__main__":
    app.run(port=5000)
