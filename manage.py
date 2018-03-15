import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db


config_name = os.environ.get('APP_SETTINGS')
app = create_app(config_name)
manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# add db command

if __name__ == "__main__":
    manager.run()