# Installation:
```
docker-compose build
docker-compose up -d
docker-compose run --rm server ./manage.py migrate
docker-compose stop
```

# Start
```
docker-compose up
```
Server will start at 8000 port

# Testing
```
docker-compose run --rm server ./manage.py test apps
```
or for local:
```
python manage.py test apps
```
