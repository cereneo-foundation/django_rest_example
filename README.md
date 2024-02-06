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

## Docker

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
## Deployments  
### Local Deployment
Clone git
````shell
$ git clone git@github.com:cereneo-foundation/django_web_template.git
$ cd django_web_template
````
Create venv
````shell
$ python -m venv venv
$ source ./venv/Scripts/activate
````
Lets jump into the './server' path, where the actual django code is stored.
````shell
$ cd ./server
````
Install requirements
````shell
$ pip install -r ./requirements.txt
````
Django_web_template depends on environment variables. The easiest way to provide them is to copy the file './server/.env.example'
````shell
$ cp .env.example .env
````
Now we can set-up the database. Since the '.env' file routes the database to a local sqlite file. Which will be created after installing our tables.
````shell
$ python manage.py migrate
````
And create a admin user
````shell
$ python manage.py createsuperuser
Username (leave blank to use 'amazing.user'): admin
Email address: test@test.ch
Password:
Password (again):
This password is too short. It must contain at least 8 characters.
This password is too common.
This password is entirely numeric.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
````
Finally, we can start django:
````shell
$ python manage.py runserver
````
We can check if everything is running. http://localhost:8000/admin
Congrats!!

### Docker deployment

Install docker https://docs.docker.com/engine/install/.
Please be aware that you need additional tools to run Docker on Windows. https://docs.docker.com/desktop/wsl/

Clone git
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
$ docker compose build 
$ docker compose up -d
````
``docker compose build`` creates runnable images from our sources.'``docker compose up`` runs the images in containers.
-d is to de-attach the docker composition for the current shell process.
You can use the command ``docker compose up --build -d`` to run in one line

We can check if everything is running. http://localhost:8000/admin
Admin user and password are by default: admin 123456
This can be changed in the ./compose.yaml file
Congrats!!

Let's stop it
````shell
$ docker compose down 
````
### Explanation

Docker builds/downloads three images.
- 'django_proxy' which serves static files (i.e. *.css, *.js) files and routes requests to 'django_server'.
- 'django_server' runs your django app with a gunicorn wsgi.
- 'postgres' runs the postgres dbms for 'django_server' to access
````shell
$ docker image 
REPOSITORY      TAG       IMAGE ID       CREATED          SIZE
django_server   latest    b34ab5c22521   35 minutes ago   222MB
django_proxy    latest    ecacf9d5acf9   2 hours ago      41.1MB
postgres        latest    b0b90c1d9579   4 weeks ago      425MB
````
With ```docker compose up``` docker starts the images in containers.
````shell
$ docker container ls
CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS                   PORTS                            NAMES
e703812f3b5d   django_proxy    "/docker-entrypoint.…"   6 minutes ago   Up 6 minutes             80/tcp, 0.0.0.0:8000->8000/tcp   django_web_template-nginx-1
f70340c49b9e   django_server   "/bin/sh -c 'python …"   6 minutes ago   Up 6 minutes                                              django_web_template-web-1
cbb0eb1e4005   postgres        "docker-entrypoint.s…"   6 minutes ago   Up 6 minutes (healthy)   5432/tcp                         django_web_template-db-1
````
Also it creates a virtual network so the different containers can communicate with leaving the HOST computer.
````shell
$ docker network ls
NETWORK ID     NAME                          DRIVER    SCOPE
64e8fb510274   bridge                        bridge    local
df52f6304d32   django_web_template_default   bridge    local
85c377eaa6f2   docker_gwbridge               bridge    local
59f5a9bac522   host                          host      local
03a8e848ad40   none                          null      local
````
Lastly it creates three virtual volumes to persistently store data.
- django_web_template_db-data: storage for postgres data files (only postgres has access)
- django_web_template_media_volume: storage for media files to store uploads (shared between django_proxy and django_server)
- django_web_template_static_volume: storage for static files. Content will be created by django_server and served by django_proxy
````shell
docker volume ls
DRIVER    VOLUME NAME
local     django_web_template_db-data
local     django_web_template_media_volume
local     django_web_template_static_volume

````