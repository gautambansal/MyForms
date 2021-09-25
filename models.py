from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)


class Forms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    creation_date = db.Column(db.Date, default = datetime.today())
    form_content = db.Column(db.Text)
    edit_form = db.Column(db.Text)
    status = db.Column(db.Boolean,nullable=False,default=True)

class Formdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('forms.id'),nullable=False)
    submission_date = db.Column(db.DateTime, default = datetime.now())
    form_data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    
    #email = db.Column(db.String(100), unique=True, nullable=False)
