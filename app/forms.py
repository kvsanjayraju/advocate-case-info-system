from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo, ValidationError
from app.models import User

class RegisterForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=1, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    bar_council_id = StringField('Bar Council ID', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ClientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=64)])
    phone_number = StringField('Phone Number', validators=[Length(max=20)])
    contact_details = StringField('Contact Details', validators=[Length(max=256)])
    notes = TextAreaField('Notes')
    submit = SubmitField('Save Client')

class CaseForm(FlaskForm):
    case_number = StringField('Case Number', validators=[DataRequired(), Length(max=64)])
    court_name = StringField('Court Name', validators=[Length(max=128)])
    case_title = StringField('Case Title', validators=[Length(max=256)])
    case_type = StringField('Case Type', validators=[Length(max=64)])
    # Client will be handled in the route, or we can add a SelectField if we want to choose from existing clients.
    # For MVP, let's assume we select client from a dropdown.
    client_id = SelectField('Client', coerce=int, validators=[DataRequired()])
    opponent_name = StringField('Opponent Name', validators=[Length(max=128)])
    opponent_advocate = StringField('Opponent Advocate', validators=[Length(max=128)])
    filing_date = DateField('Filing Date', validators=[Optional()])
    current_stage = StringField('Current Stage', validators=[Length(max=128)])
    next_hearing_date = DateField('Next Hearing Date', validators=[Optional()])
    status = SelectField('Status', choices=[('Active', 'Active'), ('Closed', 'Closed')], default='Active')
    notes = TextAreaField('Notes')
    submit = SubmitField('Save Case')
