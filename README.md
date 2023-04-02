# jobs_restapi
This is a job management Restful API project for college assignment.
You can pull an image of this project from Docker Hub using:
```bash
docker pull curaposterior/jobs_restapi:jobs_restapi
```

## Key Features

* Python FastAPI Framework
* [Docker](https://www.docker.com/)
* [Alembic](https://alembic.sqlalchemy.org/en/latest/) database migration tool
* [SQLAlchemy](https://www.sqlalchemy.org/) ORM
* JWT tokens
* Relational database (PostgreSQL)

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com), [Python](https://www.python.org/) and [Docker](https://www.docker.com/) (if you run this on Linux you should also install docker-compose) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/curaposterior/jobs_restapi

# Go into the repository
$ cd jobs_restapi

# Create virtual environment (install virtualenv if you haven't done it already)
$ python -m venv venv

# Activate virtual environment ()
$ source venv/bin/activate 

# Install packages
(venv) $ pip install -r requirements.txt

# Run the app and the database
(venv) $ docker-compose up --build -d

# After creating and running the containers create tables in database using alembic
# Make sure that you are in virtual environment
(venv) $ alembic upgrade head
```


> **Note 1**
> You also need to create .env file with required credentials.
> Example template below:
```bash
POSTGRES_USER="" #change this to your prefrences
POSTGRES_PASSWORD="" #change this to your prefrences
POSTGRES_DB="" #change this to your prefrences

DATABASE_ENGINE="postgresql"
DATABASE_HOSTNAME="db" #works only if database is in the same docker network as app container
DATABASE_USERNAME="" #change this to your prefrences
DATABASE_PASSWORD="" #change this to your prefrences
DATABASE_PORT=""  #change this to your prefrences
DATABASE_DB="" #change this to your prefrences
DATABASE_ALEMBIC_HOST="localhost"

SECRET_KEY="" #change this
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="" #change this to your prefrences
```

> **Note 2**
> You have to add trigger manually
> You can do it by connecting to the container and using psql terminal
```bash
$ docker exec -it container_name /bin/bash

root:~# psql -U username -d database_name

# paste the code from the trigger.sql file (first the function then the trigger code)
```

> **Note 3**
> If you have any trouble connecting alembic to the database check the alembic/env.py file

## Credits

This software uses code from:

- [API tutorial](https://youtu.be/0sOvCWFmrtA)
- [FastAPI documentation](https://fastapi.tiangolo.com/)


## License

MIT

---

> GitHub [@curaposterior](https://github.com/curaposterior) &nbsp;&middot;&nbsp;
