from burnermail import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    burner_emails = db.relationship('BurnerEmail', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.date_created}')"

class BurnerEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    burner_email = db.Column(db.String(128), unique=True, nullable=False)
    forwards_to = db.Column(db.String(128), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"BurnerEmail('{self.id}', '{self.burner_email}', {self.forwards_to}, {self.date_created}'"