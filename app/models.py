from . import db
from . import login_manager
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


# model definition
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    # user refers to the instance of the class Role
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, value):
        if not self.has_permission(value):
            self.permissions += value

    def remove_permission(self, value):
        if not self.has_permission(value):
            self.permissions -= value

    def reset_permission(self):
        self.permissions = 0

    def has_permission(self, value):
        return self.permissions & value == value

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Admin': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
        }
        default_role = 'User'
        for role in roles:
            get_role = Role.query.filter_by(name=role).first()
            if get_role is None:
                get_role = Role(name=role)
            get_role.reset_permission()
            for perm in roles[role]:
                get_role.add_permission(perm)
            get_role.default = (get_role.name == default_role)
            db.session.add(get_role)
        db.session.commit()

    def __repr__(self):
        return "<Role %r>" % self.name


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # this is the foreign key colum for users table which refers to roles tables id column
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role_id is None:



    def generate_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({"confirm": self.id}, salt="test_salt")

    def confirm_token(self, token, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'), salt="test_salt", max_age=expiration)
        except:
            return False
        if data.get("confirm") != self.id:
            return False
        else:
            self.confirmed = True
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password=password, salt_length=10, method='pbkdf2:sha256')

    def verify_password(self, password):
        return check_password_hash(pwhash=self.password_hash, password=password)

    def __repr__(self):
        return "<User %r>" % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
