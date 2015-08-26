from flask.ext.wtf import Form
from wtforms import TextField, StringField, PasswordField, SelectField
from wtforms.validators import DataRequired


class RegisterForm(Form):
    email = StringField('email', validators=[DataRequired()])
    number = StringField('number', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class LoginForm(Form):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class ClassForm(Form):
    subject = StringField('Subject', validators=[DataRequired()])
    course_number = StringField('Course Number', validators=[DataRequired()])
    section = StringField('Section', validators=[DataRequired()])
    campus = SelectField('Campus', choices=[('B', 'Busch'), ('L', 'Livingston')], validators=[DataRequired()])
    bus = SelectField('Bus', choices=[('B', 'Busch'), ('L', 'Livingston')], validators=[DataRequired()])
    bus_stop = SelectField('Bus Stop', choices=[('B', 'Busch'), ('L', 'Livingston')], validators=[DataRequired()])
    alert_interval = SelectField('Alert Interval', choices=[('B', 'Busch'), ('L', 'Livingston')],
                                 validators=[DataRequired()])
