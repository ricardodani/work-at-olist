Installing
==========

Pre-requisites
--------------

* Docker (tested on version 18.03.1-ce)
* docker-compose (tested on version 1.12.0)
* Make

Install locally with docker
---------------------------

For convenience, a very useful Makefile is available, so, to install it all, first, build de containers with::

    make

After it, you can run the development environment, with debug tools (django debug toolbar, `ipdb` and `DEBUG=True`) available at port `8000`_::

    make run-dev

.. _8000: http://localhost:8000/

Or, to run it with a production-like environment, available at port `80`_, type::

    make run

.. _80: http://localhost/

Testing the application
-----------------------

To test the application using the Django test framework, type::

    make test

Useful commands
---------------

* Access the python shell::

    make shell

* Rebuild the docs::

    make docs

* Migrate the database::

    make migrate

* Create a admin superuser::

    make superuser

* Rebuild docker intances::

    make build
