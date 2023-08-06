from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from game_recommender.models import User
from flask_login import current_user


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=5, max=20, message="Username must be between %(min)d and %(max)d characters long.")])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(min=15, max=40, message="Email must be between %(min)d and %(max)d characters long.")])
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