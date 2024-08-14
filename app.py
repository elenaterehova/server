import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

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


@app.route("/")
def hello():
    return {"hello": "world"}


@app.route("/notes", methods=["POST", "GET"])
def handle_notes():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_note = NotesModel(title=data['title'], description=data['description'], article=data['article'])
            db.session.add(new_note)
            db.session.commit()
            return {"message": f"note {new_note.title} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
    elif request.method == 'GET':
        notes = NotesModel.query.all()
        results = [
            {
                "title": note.title,
                "description": note.description,
                "article": note.article
            } for note in notes
        ]
        return {"count": len(results), "notes": results}
@app.route("/notes/<note_id>", methods=["GET", "DELETE", "PUT"])
def handle_note(note_id):
    note = NotesModel.query.get(note_id)
    if request.method == "GET":
        try:
            response = {
                       "title": note.title,
                       "description": note.description,
                       "article": note.article
                   }
            return response
        except:
            return {"message": "error"}
    elif request.method == "DELETE":
        try:
            db.session.delete(note)
            db.session.commit()
            return {"message": "note has been deleted"}
        except:
            return {"message": "delete error"}
    elif request.method == "PUT":
        try:
                   data = request.get_json()
                   note.title = data['title']
                   note.description = data['description']
                   note.article = data['article']
                   db.session.add(note)
                   db.session.commit()
                   return {"message": f"car {note.title} successfully updated"}
        except:
            return {"message": "put error"}

    else:
        return {"message": "Request method not implemented"}

if __name__ == '__main__':
    app.run(debug=True)
