from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    phone_number = db.Column(db.String(20))
    contact_details = db.Column(db.String(256))
    notes = db.Column(db.Text)
    cases = db.relationship('Case', backref='client', lazy='dynamic')

    def __repr__(self):
        return f'<Client {self.name}>'

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String(64), index=True)
    court_name = db.Column(db.String(128))
    case_title = db.Column(db.String(256))
    case_type = db.Column(db.String(64))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    opponent_name = db.Column(db.String(128))
    opponent_advocate = db.Column(db.String(128))
    filing_date = db.Column(db.Date)
    current_stage = db.Column(db.String(128))
    next_hearing_date = db.Column(db.Date, index=True)
    status = db.Column(db.String(32), default='Active')
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<Case {self.case_number}>'

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
