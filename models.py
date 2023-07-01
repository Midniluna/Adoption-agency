from flask_sqlalchemy import SQLAlchemy
import sys

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
def get_database_uri():
     if "python3 -m unittest" in sys.argv:
         return 'postgresql:///adoption_agency_test'
     return 'postgresql:///adoption_agency'

def get_echo_TorF():
    if "python3 -m unittest" in sys.argv:
         return False
    return True

class Pet(db.Model):
    """Pet"""

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text, nullable=False, default="https://i.imgur.com/89XRpp8.png")
    age = db.Column(db.Integer, nullable=True)
    notes = db.Column (db.Text, nullable=True)
    available = db.Column (db.Boolean, default=True)
