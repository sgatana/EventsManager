from flask_restful import Resource, request
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Events, db
from app.response.responses import invalid_data

class Event(Resource):
    @jwt_required
    def get(self):
        user = current_user = get_jwt_identity()
        # user = User.query.filter_by(id=current_user).first()
        # username = user.email
        return {"message": current_user}

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        data = request.get_json()
        if not data:
            return invalid_data, 400
        name = data["name"]
        desc = data["description"]
        location = data["location"]
        date = data["event_date"]
        event = Events.query.filter_by(name=name, user_id=current_user).first()
        if event:
            return {"error": "event exists"}, 409
        post_event = Events(name=name, desc=desc, location=location, event_date=date)
        db.session.add(post_event)
        db.session.commit()
        return {"message": "{} has been added".format(name)}, 201
