from flask import Blueprint
from app import api
from .views import Register, Login


auth = Blueprint('auth', __name__)

api.add_resource(Register, 'auth/register', endpoint='register')
api.add_resource(Login, 'auth/login', endpoint='login')