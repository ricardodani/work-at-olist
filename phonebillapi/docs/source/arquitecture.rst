Arquitecture
============

Infrasctructure
---------------

This project was originally built to run inside docker containers. A nginx is responsible to handle all frontend requests and route them
to static files, documentation or the application itself. The application is written in Django 2, using PostgreSQL as database and Django
Rest Framework to the API.

A docker-compose.yml file is available to easily deploy a complete docker environement.

Code arquitecture
-----------------

The project was designed with Django best practices and great separation of responsabilities and good code patterns.
To understand how the components interact with each other, here is a summary of how they share responsabilities:

* Views

  Responsible to handle the web requests and return responses.
  They use serializers to treat the data, call backend methods and return serialized data if success or treat possible API Exceptions.

* Serializers

  Responsible to validate requests, raise validation errors and call backend model methods to return to the views.

* Models

  Responsible to represent the data tables. Also, holds instance methods that are calculated in python.

* Managers

  Responsible to hold methods that alters and fetch data.

* Exceptions

  Holds all the known API exceptions and it's status codes. This exceptions are fetched on the view to according visualization.

* Tests

  Use unit tests to test the application, isolating each of the above layers.
