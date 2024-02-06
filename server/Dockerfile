# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.11.7
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

RUN mkdir -p /var/log/gunicorn/
RUN chown appuser /var/log/gunicorn/


# Switch to the non-privileged user to run the application.
#USER appuser
# Copy the source code into the container.
#COPY django_web_template ./django_web_template
#COPY manage.py ./manage.py
COPY . .

#USER root
# Give execution rights on the cron scripts
RUN chmod 0644 /app/scripts/clear_token_cron.sh

#Install Cron
RUN apt-get update
RUN apt-get -y install cron

# Add the cron job
RUN crontab -l | { cat; echo "0 * * * * bash /app/scripts/clear_token_cron.sh"; } | crontab -

RUN mkdir ./static
RUN mkdir ./media
RUN touch error.log
RUN touch request.log
RUN chown appuser error.log
RUN chown appuser request.log
RUN chown appuser ./static
RUN chown appuser ./media
#USER appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD python manage.py migrate; python manage.py createsuperuser --no-input; python manage.py collectstatic; gunicorn 'django_web_template.wsgi' -c gunicorn.conf.py; cron
