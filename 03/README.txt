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