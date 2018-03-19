from flask_restful import Resource, request
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Events, db
from app.response.responses import invalid_data


class Event(Resource):
    @jwt_required
    def get(self):
        # user = current_user = get_jwt_identity()
        events = Events.query.all()
        if not events:
            return {"error": "no events added"}, 401
        my_event = []
        for event in events:
            all_events = {}
            all_events['name'] = event.name
            all_events['desc'] = event.description
            all_events['owner'] = event.get_user()
            my_event.append(all_events)
            # all_events = {"name": event.name, "description": event.description}
        return {"events": my_event}, 200

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
        post_event = Events(name=name, desc=desc, location=location, event_date=date, owner=current_user)
        db.session.add(post_event)
        db.session.commit()
        return {"message": "{} has been added".format(name)}, 201
