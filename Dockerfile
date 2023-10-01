FROM python:3.10.13-alpine

MAINTAINER Nikoloz Naskidashvili

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# install dependencies
RUN python -m pip install -U --force-reinstall pip
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add --virtual build-deps build-base gcc musl-dev jpeg-dev zlib-dev libffi-dev \
    && rm -rf /var/cache/apk/*

COPY requirements.txt ./requirements.txt
COPY requirements ./requirements

# install dependencies
RUN apk add build-base   # install the GCC, libc-dev and binutils packages (greenlet error)
RUN pip install --no-cache-dir -r ./requirements.txt

# Copy project files
COPY src ./src
COPY tests ./tests
COPY envs ./envs

# Copy alembic stuff
COPY ./alembic.ini ./alembic.ini
COPY ./migrations ./migrations

# migrate database
RUN alembic upgrade head

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]