# music-world
Project for managing local music band library

# Introduction

The goal of the project is to learn django by creating a simple library of music bands.

Project is written with django 4.1.6 and python 3.10.10 in mind.

![Default Home View](_screenshots/02_Index.png?raw=true "Index")


### Main features

* The project contains 5 models
![Default Home View](_screenshots/Music_world_DB_structure.jpg?raw=true "DB structure")

* For the frontend was used [Soft UI Design Django](https://github.com/app-generator/django-soft-ui-design/tree/80b06c0fef43c983693e04b1ba25211104c461f2) 

* Bootstrap and crispy forms support included

* User registration and logging are implemented

* SQLite database

# Setup

### 1. Clone project from GitHub to local computer.

Open the Git Bash console in the directory where you want to place the project. Run command:

    $ git clone https://github.com/VladyslavKlevanskyi/music-world.git

### 2. Create virtual environment

Open the project and run command:

    $ python -m venv venv
    
And then activate virtualenv:
    
a) For windows:

    $ venv\Scripts\activate
   
b) For mac:

    $ source venv/bin/activate
      

### 3. Installing project dependencies

Run command:

    $ pip install -r requirements.txt

### 4. Creating a database

To create a database, run migrations:

    $ python manage.py migrate
    
To fill the database, import the `.json` file with the command:
    
    $ python manage.py loaddata database_01.json

### 5. Adding a secret key to the project

Generate a new secret key:

    $ python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

Rename `.env_sample` file to `.env`. Open it and replace `<your_secret_key>` with the key you generated before.

### 7. Run tests

In order to make sure that the project is working correctly, run the tests with the command:

    $ python manage.py test 

### 8. Run the project

You can now run the development server:

    $ python manage.py runserver

### 9. Entrance to the music library

In the address bar of your browser, enter:

    http://127.0.0.1:8000/

On the login page enter:
* Username - `admin`
* Password - `1qazXcde3`

Enjoy!