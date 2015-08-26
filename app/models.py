""" This file contains SQL models for TextBus """

from app import db
from passlib.apps import custom_app_context as pwd_context


class CourseAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(32))
    start_time = db.Column(db.String(8))
    campus = db.Column(db.String(8))
    meeting_day = db.Column(db.String(8))
    bus_stop = db.Column(db.String(16))
    bus = db.Column(db.String(8))
    alert_interval = db.Column(db.String(8))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, start_time, campus, day, stop, bus_name, interval, user):
        self.course_title = title
        self.start_time = start_time
        self.campus = campus
        self.meeting_day = day
        self.bus_stop = stop
        self.bus_name = bus_name
        self.alert_interval = interval
        self.user = user


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    phone_number = db.Column(db.String(16), nullable=False)
    password_hash = db.Column(db.String(128), index=True)
    courses = db.relationship('CourseAlert', backref='user')

    def __init__(self, email, phone_number):
        self.email = email
        self.phone_number = phone_number

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
