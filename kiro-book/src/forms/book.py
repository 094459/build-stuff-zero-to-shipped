"""
Book-related forms for the book sharing application.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, URLField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, URL

class BookForm(FlaskForm):
    """Form for creating and editing books."""
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    author = StringField('Author', validators=[DataRequired(), Length(max=255)])
    isbn = StringField('ISBN', validators=[Optional(), Length(max=20)])
    purchase_url = URLField('Purchase URL', validators=[Optional(), URL(), Length(max=512)])
    recommendation_rating = IntegerField('Recommendation Rating (1-5)', validators=[
        DataRequired(),
        NumberRange(min=1, max=5, message='Rating must be between 1 and 5')
    ])
    is_fiction = RadioField('Category', choices=[
        ('fiction', 'Fiction'), 
        ('non-fiction', 'Non-Fiction')
    ], default='fiction')
    is_hidden = BooleanField('Hide from public dashboards', default=False)
    submit = SubmitField('Save Book')

class CommentForm(FlaskForm):
    """Form for adding comments to books."""
    comment_text = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add Comment')

class BorrowRequestForm(FlaskForm):
    """Form for requesting to borrow a book."""
    submit = SubmitField('Request to Borrow')
