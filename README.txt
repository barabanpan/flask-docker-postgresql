Done by this tutorial:
https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx

1. Create little Flask app.
Uses flask.cli.FlaskGroup. It has a decorator that allows using functions as cmd commands.
Try like this:  python manage.py do_fun
Run like this: 
export FLASK_APP=project/__init__.py
python manage.py run

2. Add Docker.
Install Docker with this instruction or any similar:
https://www.digitalocean.com/community/tutorials/docker-ubuntu-18-04-1-ru
Install Docker Compose with this instruction or any similar:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-ru
Add Dockerfile to web directory, 
docker-compose.yml and .env.dev to root directory.
Build, run container and shut it.

3. Add PostgreSQL.
Do a lot of db-related things:)
Useful commands:
docker-compose exec web python manage.py create_db
docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev
docker volume ls
Thanks to volume, changes in db should stay after rebuild.

3.1 Fix missing things:)
Also add entrypoint.sh script where you can verify that postgres is up and doing okay before creating tables or starting app.

4. Add gunicorn for production
Create docker-compose.prod.yml, .env.prod, .env.prod.db and add two latter to .gitignore.
Run: docker-compose -f docker-compose.prod.yml up -d --build

5. Add production Dockerfile
Dockerfile.prod creates new user for security reasons and also runs some other things needed for production. Large and complicated file:)

6. Add Nginx
That's a reverse proxy server. It's there to support static files. At this point it's just there and recieves requests. 
You need to add a nginx service to docker-compose.prod.yml and create nginx folder in services. It should contain Dockerfile and nginx.conf.

7. Add static files support via nginx
Add volume to docker-compose.prod.yml, create folder 'static'. Development doesn't need a volume.

8. Add media files support via nginx
Media files are files uploaded by user. Do things like in step 7.

9. Add celery and redis for dev
And send some emails!!!
For dev:
 - make celery-redis functionality
 - add celery and redis services to docker-compose. Celery and web depend on redis. Hint: celery imports from web directory, so that they are configured as almost same container, but are different. To avoid building same thing twice moved celery to web container. Runs with two commands, first is detached.

9.1. Add celery and redis for prod

TODOS:
- celery wants non root user for safety reasons, redis wants some config file.



.env.dev and .env.prod should look like this:
FLASK_APP=project/__init__.py
FLASK_ENV=development
DATABASE_URL=postgresql://abc:your_pass@db:5432/db_name
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
APP_FOLDER=/usr/src/app

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

MAIL_USERNAME=your.email@example.com
MAIL_PASSWORD=your_pass


.env.pro.db should look like this:
POSTGRES_USER=my_user
POSTGRES_PASSWORD=my_user_pass
POSTGRES_DB=db_name

