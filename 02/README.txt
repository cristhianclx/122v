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