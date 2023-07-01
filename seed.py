from app import db, app
from models import Pet

app.app_context().push()

db.drop_all()
db.create_all()

a = Pet(name="Bucky", species="cat", photo_url="https://i.imgur.com/abpSwBL.jpeg")
b = Pet(name="Bunnie", species="other", photo_url="https://i.imgur.com/BjRuUVD.jpeg")
c = Pet(name="Polite Maxwell", species="dog", photo_url="https://i.imgur.com/YOo9TdX.jpeg")
d = Pet(name="Evil Maxwell", species="dog", photo_url="https://i.ytimg.com/vi/S0pZEMxyrgk/maxresdefault.jpg")


db.session.add(a)
db.session.add(b)
db.session.add(c)
db.session.add(d)
db.session.commit()