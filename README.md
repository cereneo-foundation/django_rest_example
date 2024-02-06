# django_web_template

This template provides a setup to easily develop RESTFUL servers.
It implements following features:
## Features

### Security

- User Management Backend (http://localhost:8000/admin)
    - Create Users / Groups
    - Define permissions
    - Block authorization (Tokens)
    - https://docs.djangoproject.com/en/5.0/ref/contrib/admin/
- JWT Authorization
    - Is used to authorize REST clients with user credentials
    - https://django-rest-framework-simplejwt.readthedocs.io/en/latest/
- Role-based access restrictions
    - restricting access based on roles
    - Model level permission
    - https://www.django-rest-framework.org/api-guide/permissions/
- Access-log
    - Needed for sensitive data
    - Every request will be logged with username and IP

### Database

- Object–relational mapping (ORM)
    - Helpful tool to use database table in objects
    - Mapping Classes to Data Table
    - https://docs.djangoproject.com/en/5.0/topics/db/models/
- Database migration
    - Easy set-up of databases
    - https://docs.djangoproject.com/en/5.0/topics/migrations/

### Webservice

- Apps
    - Django method to split functionalities
    - https://docs.djangoproject.com/en/5.0/ref/applications/
- Django REST framework
    - Clean structure of functionalities
    - Serialization of model objects
      - https://www.django-rest-framework.org/api-guide/serializers/
    - Hyperlink based Model object relations
        - https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    - Class based view handlers
      - https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    - https://www.django-rest-framework.org/
- Browsable Swagger API
  - http://localhost:8000/swagger
  - http://localhost:8000/redoc
  - https://drf-yasg.readthedocs.io/en/stable/

### Examples

- Simple example of storing Patient Appointment data
    - can be found in ./server/django_web_template/appointment
- Simple example for a client
    - found in client/login_test.py
    - needs 'requests' library

### Deployment

- Deployment ready Docker set up
  - Django -> Gunicorn -> nignx set-up
  - Django -> Postgres set-up
  - Django container cron job
- Tool to create and personalize docker composition settings and generate password / secret_key
  - ./install_scripts/create_docker_env.py
- Docker secrets for passwords secret_key
  - https://docs.docker.com/compose/use-secrets/
- Docker compose file to run standalone
  - https://docs.docker.com/compose/

## Install on docker

install docker 

clone git
````shell
$ git clone git@github.com:cereneo-foundation/django_web_template.git
````

