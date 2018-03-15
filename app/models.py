import datetime, jwt
from app import db, app_config
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True)
    email = db.Column(db.String(140), index=True, unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return 'users: {}'.format(self.username)

    def encode_auth_token(self, user_id):
        """
        Generates auth token
        :param user_id:
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(payload,
                              current_app.config.get('SECRET_KEY'),
                              algorithm='HS256'
                              )

        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param: auth_token
        :return: string/ integer
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            print(current_app)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired, please log in'
        except jwt.InvalidTokenError:
            return 'Invalid token, please log in agian'
