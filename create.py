from market.models import db, Category

db.session.add(Category(name="Koszykówka - punkty", full_name="Koszykówka - punkty"))
db.session.commit()
# db.drop_all()
# db.create_all()
