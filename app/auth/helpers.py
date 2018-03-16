from flask_jwt_extended import create_access_token
from app import jwt
import datetime

blacklist = set()


def auth_token(id):
    expires = datetime.timedelta(hours=1)
    token = create_access_token(id, expires_delta=expires)
    return token


# @jwt.token_in_blacklist_loader
# def check_if_token_in_blacklist(decrypted_token):
#     jti = decrypted_token['jti']
#     return jti in blacklist