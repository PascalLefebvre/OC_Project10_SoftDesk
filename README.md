# Openclassrooms - Project 10 : Create a RESTful secure API using Django REST

    The Issue tracking system is an API for reporting and monitoring technical problems.
	

## Installation


* After cloning, change into the directory and type :
    
    	'python -m venv env'.

* Next, enter in your virtual environment :
    
    	'source env/bin/activate' (to deactivate, type 'deactivate')

* Install all the necessary packages :
    
    	'python -m pip install -r requirements.txt'
    
* Generate the secret key and save it in a file named ".env" :
    
    	'python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key()) > .env'
    	
* Sync the database with Django’s default settings :
    
    	'python manage.py migrate'
    
* Start up the local Django web server :
    
    	'python manage.py runserver' (the API should respond with the default address "http://127.0.0.1:8000")


## The API documentation

* [Access to the API documentation here](https://documenter.getpostman.com/view/25323756/2s935kN5WP)

