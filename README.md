# Starnavi Test project
The project allows to signup users, create posts and set likes/unlikes. Some features:
  - bot-autofiller included
  - schema of an api is available at /schema/ url. To see all the fields please uncomment SessionAuthentication in settings.py
  - Clearbit user enrichment implemented, but disabled because of restrictions
  - Email deliverability is checked by emailhunter.co

### Installation

Project tested with Python3.6.1. Database should be Postgres, as JSONField is used.
Clone repository, create virtualenv and install the project:

```sh
$ cd starnavi
$ pip install -r requirements.txt
```
Create local_settings.py file from local_settings.py_:
```$sh
$ cp starnavi/local_settings.py_ starnavi/local_settings.py
```
Fill in local_settings.py with your preferences and API keys.
Apply migrations:
```sh
$ python manage.py migrate
```
Finally, run the server:
```sh
$ python manage.py runserver
```
### How to use bot
Run the command:
```sh
python manage.py run_bot
```
Bot uses [requests](https://github.com/kennethreitz/requests) library for reaching api endpoints. Settings of the bot are placed at the bottom of the settings file (or local_settings.py). Feel free to change NUMBER_OF_USERS, MAX_POSTS_PER_USER, MAX_LIKES_PER_USER, as well as TEST_DOMAIN.
