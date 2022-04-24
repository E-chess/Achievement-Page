from flask_login import UserMixin

from market import db, bcrypt, login_manager


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    value = db.Column(db.String(), nullable=False)
    participants = db.Column(db.String(), nullable=False)
    school_name = db.Column(db.String(), db.ForeignKey('school.id'))
    category = db.Column(db.String(), nullable=False)
    date_of_do = db.Column(db.String())
    description = db.Column(db.String())
    link = db.Column(db.String())
    date_of_add = db.Column(db.String(), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'


class School(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=5), unique=True)
    full_name = db.Column(db.String(), unique=True)


class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True)
    full_name = db.Column(db.String(), unique=True)
