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

Install docker https://docs.docker.com/engine/install/.
Please be aware that you need additional tools to run Docker on Windows. https://docs.docker.com/desktop/wsl/

clone git
````shell
$ git clone git@github.com:cereneo-foundation/django_web_template.git
$ cd django_web_template
````

create necessary docker environment files 
````shell
$ python ./install_scripts/create_docker_env.py
````
Follow the instructions:
````
Welcome to docker environment creation
Creating .env file for docker
Define Hostname from which django will server (leave blank to use 'localhost'): localhost
Define Host port from which django will server (leave blank to use '8000'): 123456
Be sure you change the 'nginx.conf' to listen to the same port and 'docker-compose.yml' to map nginx to the same port
Define Protocol which django will server (leave blank to use 'http'): http
Postgres Database name (leave blank to use 'django'): django
Postgres Username (leave blank to use 'django'): django
Postgres Password (leave blank to generate):
.env to ..
DB pw written to ..\secrets
DB url written to ..\secrets
Secret key written to ..\secrets
````
Please be aware that you need to manually change the listen port in '/nginx/nginx.conf' and the mapping in /compose.yaml
````
server {

    listen 12345;
    location /static/ {
        alias /var/staticfiles/;
    }

    location /media/ {
        alias /var/mediafiles;
    }

    location / {
        limit_req zone=mylimit burst=20 nodelay;
        real_ip_header X-Forwarded-For;
        real_ip_recursive on;
        proxy_pass http://web_app;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Host $http_host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Port $server_port;
        proxy_set_header Host $host:$server_port;
        proxy_redirect off;
    }

}
````
````yaml
  nginx:
    image: django_server
    build: ./nginx
    restart: always
    ports:
      - ${PORT}:12345
    volumes:
      - static_volume:/var/staticfiles
      - media_volume:/var/mediafiles
    depends_on:
      - web
````
This script will create the file .env in the root folder which general variables for the docker compose file and secrets 
in /secrets which are needed to securely store passwords and are then used in the compose process.

Next we build and run the composition
````shell
$ docker compose up --build -d
````
The parameter --build is to force build the different containers.
-d is to de-attach the docker composition for the current shell process.

