from flask_wtf import Form
from wtforms import HiddenField, SelectField, StringField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import TextArea

from wedding_site.models.constants import *


class AddUserForm(Form):
    email = EmailField('Email', validators=[DataRequired()])
    first_name = StringField('First name')
    last_name = StringField('Last name')
    invitation_iid = HiddenField('Invitation iid')
    invitation_size = IntegerField('Invitation size', default=1,
                                   validators=[NumberRange(min=1, max=10)])
    invitation_status = SelectField('Invitation status', coerce=int,
                                    choices=[(INVITED_BOTH, 'Day and evening'),
                                             (INVITED_DAY, 'Day only'),
                                             (INVITED_EVENING, 'Evening only')])


class EditNameForm(Form):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])


class GenderForm(Form):
    gender = SelectField('Gender', choices=[('male', 'Male'),
                                            ('female', 'Female'),
                                            ('other', 'Other')])
    other = StringField('Specify other')


class GroupForm(Form):
    group = SelectField('Group', coerce=int)
    group_name = StringField('Group name')


class DietaryRequirementsForm(Form):
    dietary_requirements = StringField('Dietary requirements',
                                       widget=TextArea())
