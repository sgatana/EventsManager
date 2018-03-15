from app.models import User, db


def add_user(username, email, password):
    user = User(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    return user

