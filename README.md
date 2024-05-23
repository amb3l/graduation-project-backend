# graduation-project-backend
# Usage guide
## Dependencies installation
```
pip install pipenv

pipenv shell

pipenv install
```
## Database creation
```
python manage.py makemigrations users

python manage.py makemigrations platform_app

python manage.py makemigrations

python manage.py migrate
```
## Starting the server
```
python manage.py runserver
```