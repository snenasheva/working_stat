import jwt
from app import db, bcrypt, login_manager
from flask_login import UserMixin
from flask import current_app
from datetime import datetime, timedelta


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String, nullable=False)  # Admin, Manager, etc.
    email = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    employees = db.relationship('Employee', backref='added_by', lazy=True)

    def has_role(self, *roles):
        return self.role in roles

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, text_password):
        self.password_hash = bcrypt.generate_password_hash(text_password).decode('utf-8')

    def check_login_psw(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def get_reset_psw_token(self, expires_in=600):
        expiration_time = datetime.utcnow() + timedelta(seconds=expires_in)
        return jwt.encode(
            {'reset_password': self.id, 'exp': expiration_time.timestamp()},
            current_app.config['JWT_SECRET_KEY'], algorithm='HS256'
        )

    @staticmethod
    def verify_reset_psw_token(token):
        try:
            id = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(User, id)

    def __repr__(self):
        return f'{self.username}'


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    office = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    exception = db.Column(db.Boolean, default=False)
    hours_month = db.Column(db.Integer)
    office_visits = db.Column(db.Integer)
    added_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.name} {self.last_name}'
