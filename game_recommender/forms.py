from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, FieldList
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from game_recommender.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=5, max=20, message="Username must be between %(min)d and %(max)d characters long.")])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords do not match.")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError("That username is taken. Please choose a different one")
    
    def validate_email(self, email):
        existing_user = User.query.filter_by(email=email.data).first()
        if existing_user:
            raise ValidationError("That email is taken. Please choose a different one")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=5, max=20, message="Username must be between %(min)d and %(max)d characters long.")])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            existing_user = User.query.filter_by(username=username.data).first()
            if existing_user:
                raise ValidationError("That username is taken. Please choose a different one")
    
    def validate_email(self, email):
        if email.data != current_user.email:
            existing_user = User.query.filter_by(email=email.data).first()
            if existing_user:
                raise ValidationError("That email is taken. Please choose a different one")


class RecommenderFrom(FlaskForm):
    games = FieldList(StringField("Game Name", validators=[DataRequired()]), min_entries=5)
    submit = SubmitField("Recommend")

