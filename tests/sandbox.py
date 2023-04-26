import jwt, datetime, os
from app import create_app



app = create_app(os.getenv('FLASK_CONFIG') or 'default')


def generate_confirmation_token(expiration=600):
    reset_token = jwt.encode(
        {
            "confirm": id,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                   + datetime.timedelta(seconds=expiration)
        },
        app.config['SECRET_KEY'],
        algorithm="HS256"
    )
    return reset_token

test = generate_confirmation_token()
print(test)