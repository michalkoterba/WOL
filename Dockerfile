FROM python:alpine

# Aktualizuję menadżer repo
RUN apk update
RUN apk upgrade
RUN apt add iputils

# Tworzę i przechodzę do katalogu app
RUN mkdir /app
RUN mkdir /app/Setup
RUN mkdir /app/templates
WORKDIR /app

# kopiuję pliki źródłowe
ADD . .
ADD ./templates/* ./templates/

# Upgrade pip
RUN python -m pip install --upgrade --no-cache-dir pip

# Instaluję pakiety python
RUN pip install -r ./requirements.txt

# Ustawiam wykonywalność dla website.py
RUN chmod +x flask_app.py

ENTRYPOINT [ "python3","/app/flask_app.py"]
