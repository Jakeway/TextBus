__author__ = 'jakeway'

from flask import render_template, request, redirect, session, url_for, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from rutgers import Soc
from .forms import LoginForm, RegisterForm, ClassForm
from .models import User, CourseAlert


@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
def index():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user is not None:
            if user.verify_password(password):
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('home'))
    return render_template('index.html', title='Welcome', form=form)


@app.route('/home', methods=['GET'])
def home():
    if g.user is None or not g.user.is_authenticated():
        return redirect(url_for('login'))

        # get classes for user here
        # classes = g.user.get_classes()
    return render_template('home.html', title='Home')


@app.route('/addclass', methods=['GET', 'POST'])
def add_class():
    if g.user is None or not g.user.is_authenticated():
        return redirect(url_for('login'))
    soc = Soc()
    subjects = soc.get_subjects()
    form = ClassForm()
    if form.validate_on_submit():
        subj = form.subject.data
        course_num = form.course_number.data
        section = form.section.data
        campus = form.campus.data
        bus = form.bus.data
        bus_stop = form.bus_stop.data
        alert_interval = form.alert_interval.data
    return render_template('addclass.html', title='Add Class', form=form, subjects=subjects)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user is not None:
            if user.verify_password(password):
                db.session.add(user)
                db.session.commit()
                login_user(user)
                print email + ' has been authenticated'
                return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        number = form.number.data
        password = form.password.data
        if User.query.filter_by(email=email).first() is not None:
            return render_template('error.html', title='Error',
                                   error='another user has already registered with that email',
                                   solution='Please use a different email address')
        user = User(email=email, phone_number=number)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return render_template('home.html')
    return render_template('register.html', title='Register', form=form)
