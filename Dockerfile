FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /dataox

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


COPY ./Pipfile ./Pipfile.lock ./

RUN pip install --upgrade pip
RUN pip install --upgrade pipenv
RUN pipenv install

COPY . ./