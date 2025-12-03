"""
Profile-related forms for the book sharing application.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class ProfileForm(FlaskForm):
    """Form for editing user profile."""
    alias = StringField('Display Name', validators=[DataRequired(), Length(min=3, max=100)])
    bio = TextAreaField('Biography', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Update Profile')