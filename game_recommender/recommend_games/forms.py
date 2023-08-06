from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList
from wtforms.validators import DataRequired


class RecommenderForm(FlaskForm):
    games = FieldList(StringField("Game Name", validators=[DataRequired()]), min_entries=5)
    submit = SubmitField("Recommend")