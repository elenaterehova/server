import os

from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
DATABASE_URI = os.getenv("DATABASE_URI")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class NotesModel(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    article = db.Column(db.String())

    def __init__(self, title, description, article):
        self.title = title
        self.description = description
        self.article = article

    def __repr__(self):
        return f"<Note {self.title}"
