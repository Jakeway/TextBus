__author__ = 'jakeway'

""" This file contains SQL models for TextBus """

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
db = SQLAlchemy(app)


class CourseAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(32))
    start_time = db.Column(db.String(8))
    campus = db.Column(db.String(8))
    meeting_day = db.Column(db.String(8))
    bus_stop = db.Column(db.String(16))
    bus_name = db.Column(db.String(8))
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
    email = db.Column(db.String(256))
    phone_number = db.Column(db.String(16))
    password_hash = db.Column(db.String(128), index=True)
    courses = db.relationship('Course', backref='user')

    def __init__(self, email, phone_number):
        self.email = email
        self.phone_number = phone_number

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
