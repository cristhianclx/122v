# virtualenv

python -m venv .venv
.venv\Scripts\activate.bat # activate.ps

# install

pip install -r requirements.txt --upgrade

# utils

pip freeze
pip install Flask

# flask

flask --app main run --reload

# database

flask --app main db init # init
flask --app main db migrate # create migration
flask --app main db upgrade # apply
flask --app main db downgrade # revert apply

# shell

flask --app main shell

>>> from main import db, User
>>> item = User(first_name="cristhian", last_name="cueva", age=33, country="PE", city="Lunahuana")
>>> db.session.add(item)
>>> db.session.commit()

>>> from main import db, User
>>> User.query.all()

>>> from main import db, User
>>> User.query.get_or_404(2)
>>> User.query.filter_by(id=2).first()
>>> User.query.filter_by(first_name="alan").first()

>>> from main import db, User
>>> item = User.query.get_or_404(2)
>>> item.city = "New York"
>>> db.session.add(item)
>>> db.session.commit()

>>> from main import db, User
>>> item = User.query.get_or_404(2)
>>> db.session.delete(item)
>>> db.session.commit()