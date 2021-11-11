from market import db


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    value = db.Column(db.Integer(), nullable=False)
    unit_of_value = db.Column(db.String())
    school_name = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())

    def __repr__(self):
        return f'Item {self.name}'
