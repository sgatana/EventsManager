from flask import Blueprint
from .views import Event
from app import api


event = Blueprint('event', __name__)

api.add_resource(Event, 'events')