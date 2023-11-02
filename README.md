# task_manager

## Setup
The first thing is cloneing the repository:
```sh
$ git clone https://github.com/MdAshiqurRahmanZayed/task_manager.git
$ cd task_manager 
```
Create a virtual environment to install dependencies in and activate it (This is for linux User):
```sh
$ python -m venv env
$ source env/bin/activate
```
Then install the dependencies:
```sh
(env)$ pip install -r requirements.txt
```
Create a Database in PostgreSQL.
Create info.py in the task_manager folder just like info-demo.py and fill in the equivalent answer (DJANGO_SECRET_PASSWORD ,DATABASE_NAME ,DATABASE_PASSWORD ,DJANGO_SECRET_PASSWORD ) You can create DJANGO_SECRET_PASSWORD from this website https://djecrety.ir/. <br>
We have to migrate.
```sh
(env)$ python manage.py makemigrations 
(env)$ python manage.py migrate 
(env)$ python manage.py createsuperuser
```
```sh
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`<br>
