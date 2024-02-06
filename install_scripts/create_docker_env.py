import os
import secrets

SECRETS_DIR = os.path.join("..", "secrets")
WEB_STANDARD_HOST_NAME = "localhost"
WEB_STANDARD_PORT = 8000
WEB_STANDARD_PROTOCOL = 'http'

DOCKER_COMPOSE_DIR = '..'
DOCKER_ENV_FILE_TEMPLATE = "DB_NAME='%(name)s'\n" + \
                           "DB_USER='%(user)s'\n" + \
                           "HOSTNAME='%(host)s'\n" + \
                           "PORT=%(port)s\n" + \
                           "PROTOCOL='%(protocol)s'"

POSTGRES_STANDARD_USER = "django"
POSTGRES_STANDARD_DATABASE = "django"
POSTGRES_PASSWORD_LENGTH = 13

DJANGO_SECRET_LENGTH = 50
DJANGO_STANDARD_ADMIN_NAME = "admin"
DJANGO_DATABASE_URL = 'postgresql://%(user)s:%(pw)s@db:5432/%(name)s'


def _write_to_file(base_dir, filename, content):
    f = open(os.path.join(base_dir, filename), "w")
    f.write(content)
    f.close()


def create_docker_env():
    postgres_user = POSTGRES_STANDARD_USER
    postgres_database = POSTGRES_STANDARD_DATABASE
    postgres_pw = secrets.token_hex(POSTGRES_PASSWORD_LENGTH)
    host_name = WEB_STANDARD_HOST_NAME
    port = WEB_STANDARD_PORT
    protocol = WEB_STANDARD_PROTOCOL

    docker_env = DOCKER_ENV_FILE_TEMPLATE % {'name': postgres_database,
                                             'user': postgres_user,
                                             'host': host_name,
                                             'port': port,
                                             'protocol': protocol}
    database_url = DJANGO_DATABASE_URL % {'name': postgres_database, 'user': postgres_user, 'pw': postgres_pw}

    _write_to_file(DOCKER_COMPOSE_DIR, ".env", docker_env)
    print(f".env to {DOCKER_COMPOSE_DIR}")

    _write_to_file(SECRETS_DIR, "db.key", postgres_pw)
    print(f"DB pw written to {SECRETS_DIR}")

    _write_to_file(SECRETS_DIR, "db_url.key", database_url)
    print(f"DB url written to {SECRETS_DIR}")


def create_secret_key():
    # generating and printing the SECRET_KEY
    secret_key = secrets.token_urlsafe(DJANGO_SECRET_LENGTH)
    _write_to_file(SECRETS_DIR, "secret.key", secret_key)
    print(f"Secret key written to {SECRETS_DIR}")


def main():
    if not os.path.exists(SECRETS_DIR):
        os.mkdir(SECRETS_DIR)
    create_docker_env()
    create_secret_key()


if __name__ == "__main__":
    main()
