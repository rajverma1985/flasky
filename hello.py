from flask import Flask

app =Flask(__name__)


@app.route('/')
def hello():
    return f'Welcome to Flask'


@app.route('/username/<user>')
def user(user):
    return f'<h1>Hello {user}</h1>'






if __name__=="__main__":
    app.run(port=5000)
