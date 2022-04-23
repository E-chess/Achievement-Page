from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

from market.models import User, Item, School, Category


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='Nazwa urzytkownika:', validators=[DataRequired()])
    password = PasswordField(label='Hasło:', validators=[DataRequired()])
    submit = SubmitField(label='Zaloguj')


class AddForm(FlaskForm):
    @staticmethod
    def validate_name(self, name_to_check):
        item = Item.query.filter_by(name=name_to_check.data).first()
        if item:
            raise ValidationError('Rekord o takiej nazwie już istnieje, musisz wybrać inną')

    school_list = []
    for school in School.query.all():
        school_list.append((school.name, school.full_name))

    category_list = []
    for category in Category.query.all():
        category_list.append((category.name, category.full_name))

    name = StringField(label='Nazwa rekordu', validators=[DataRequired()])
    value = StringField(label='Wartość rekordu', validators=[DataRequired()])
    participants = StringField(label='Uczestnicy', validators=[])

    school_name = SelectField(label='Nazwa szkoły',
                              choices=school_list,
                              validators=[DataRequired()])

    # Kategorie
    category = SelectField(label='Kategoria',
                           choices=category_list,
                           validators=[DataRequired()])

    # Data zrobieni rekordu rozłożona na czyniki pierwsze
    date_of_do_year = StringField(label='Data wykonania', validators=[DataRequired()])
    date_of_do_month = StringField(label='', validators=[DataRequired()])
    date_of_do_day = StringField(label='', validators=[DataRequired()])

    # Opis
    description = TextAreaField(label='Opis')

    # Link
    link = StringField(label='link')

    # Akceptacja
    submit = SubmitField(label='Dodaj')
