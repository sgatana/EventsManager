from flask import jsonify, request, make_response
from flask_restful import Resource
from app.models import User, db
from .helpers import auth_token


class Register(Resource):
    def post(self):
        post_data = request.get_json()
        if not post_data:
            return make_response(jsonify({"error": "invalid data"}), 400)
        username = post_data.get('username')
        email = post_data.get('email')
        password = post_data.get('password')
        user = User.query.filter_by(email=email).first()
        if user is not None:
            return make_response(jsonify({"error": "user already exists"}), 409)
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"message": "registration successful"}), 201)


class Login(Resource):
    def post(self):
        post_data = request.get_json()
        if not post_data:
            return {"error": "input data is not a valid format"}, 400
        try:
            email = post_data['email']
            password = post_data['password']
            user = User.query.filter_by(email=email).first()
            if user:
                user.verify_password(password)
                access_token = auth_token(user.id)
                return make_response(jsonify({"message": "login successful", "token": access_token}), 200)
            return {"error": "login unsuccessful, use a valid email address"}, 401
        except Exception as e:
            return {"error": "please enter valid input data"}


