# alpine is a minimal image, good for production    And also it has no unnecessary dependencies
FROM python:3.9-alpine3.13
# Who is maintaining this image
LABEL maintainer="Matyas Sina"

# This is for telling python to not buffer outputs    so that we can see the output of our application in real time or speed up the logging
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /temp/requirements.txt
COPY ./requirements.dev.txt /temp/requirements.dev.txt
COPY ./app /app
# Switching to the working app directory
WORKDIR /app
# Expose port 8000 to the outside world(from the container to the host machine/local machine)
EXPOSE 8000

ARG DEV=false
# This is to safeguard against any conflicts with the system python packages
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # this is the client pkg that we gonna need to install in "alpine" base image
    apk add --update --no-cache postgresql-client && \
    # naming the grouped dependencies called ".tmp-build-deps"    that is the reason we used "--virtual"
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /temp/requirements.txt && \
    # This(shell cmd) is magic happens which updates from docker compose file    If the DEV argument is true
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /temp/requirements.dev.txt; \
    fi && \
    # To make the Docker image as lightweight as possible, we remove the temp requirements file
    rm -rf /temp && \
    # look at this deleting dependencies after "used it"!!! WOALA
    apk del .tmp-build-deps && \
    # adding a "new user" inside image, because best practice not to use "root user"    [FOR SECURITY REASONS]
    adduser \
        # we don't need to use password to this, not loging to the container using the password
        --disabled-password \
        # don't create home directory
        --no-create-home \
        # You can use any name
        django-user

# This is defining the directories all executables will be running from,    so whenever we run any python or pip command, it will use /py/bin/python or /py/bin/pip
ENV PATH="/py/bin:$PATH"

# Switching to the new user we created
USER django-user