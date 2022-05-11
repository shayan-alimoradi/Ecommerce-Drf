# Ecommerce Drf
*This repo implements an Ecommerce app that uses **Django Rest Framework** as a rest-api*

## Technologies used in this project

```
    Python 3.9 - Programming Language
    Django 4.0.x - Web Framework
    Django Rest Framework - Web API's
    Docker - Container Platform
    Pytest - Testing tool
    Git - Version Control
    PostgreSQL - PostgreSQL Database
    Celery - Asynchronous task queue
    RabbitMQ - Message Broker
    NginX - Web Server
    Gunicorn - WSGI Http Server
    Poetry - Dependency management and packaging
```

## Installation

First **clone** or **download** this project.
```
$ git clone https://github.com/Shayan-9248/Ecommerce-Drf.git
```

Then download and install docker and docker-compose

* [docker](https://docs.docker.com/engine/install/)
* [docker-compose](https://docs.docker.com/compose/install/)  

Now run the project with **docker-compose**.
```
$ docker-compose up
```

If you want to run in the background
```
$ docker-compose up -d
```

*You can see the list of all the API's from this url: **localhost:82/swagger/***

*And for more details and information about API's such as `Input data`*
*and `Response data` go to this address: **localhost:82/redoc/***

*API's are accessible by docker containers which you can see with below command.*
```
$ docker ps -a
```