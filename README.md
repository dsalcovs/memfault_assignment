Firstly I'd like to thank whoever is taking the time to review my assignment. It's not easy to do them and it's not easy
to review them either. I appreciate you taking the time to do so and I hope my instruction are as accurate as possible.


Setup

1. In your postgres server create our database by running `CREATE DATABASE memfault_assignment`
2. Decompress the git archive into the working directory of your choice and navigate to that directory on your terminal
3. Within the directory run `poetry install` # poetry is our dependency management tool
4. Activate the virtual environment by running `poetry shell`
5. Run `alembic init alembic` # This is our tool to create the DB schema in a repeatable way that keeps track of changes
6. Run `alembic upgrade head` # This creates our DB schema
7. Start the flask server by running `flask run` within our poetry shell
8. Create test data in the database by running `curl "localhost:5000/populate_database`
      a. This can be run multiple times as needed to reset the DB. It will delete all data before inserting. 

Now we can start sending requests to the server!!! 

1. upload_firmware_update will allow devices to upload a firmware update
Here are some sample requests and the expected responses

`curl "localhost:5000/upload_firmware_update -d {"device_id": 1, "secret": "AAA", "version": "SemVer1.1"} -H 'Content-Type: application/json`
This should return "Successfully updated firmware version". The new row should be visible in our device_firmware_updates table.

`curl "localhost:5000/upload_firmware_update -d {"device_id": 1, "secret": "AAB", "version": "SemVer1.1"} -H 'Content-Type: application/json`
This is the wrong secret, so it should return "Invalid Request". The vague response is intentional as this is a security rejection.

`curl "localhost:5000/upload_firmware_update -d {"device_id": 1, "secret": "AAA", "version": "SemVer11"} -H 'Content-Type: application/json`
This should return "Version string formatting not valid" as the version string is not within the format described in the requirements.

2. get_firmware_updates_by_device_id will allow an authorized user to retrieve all firmware updates for a particular device

`curl "localhost:5000/get_firmware_updates_by_device_id?email=diegosalcovsky@gmail.com&device_id=1&secret=ABC"`
This should return a JSON with the list of firmware updates for the first device in the database. There's one 
already create by `populate_database`, but more will be returned if you've added them with `upload_firmware_update`

`curl "localhost:5000/get_firmware_updates_by_device_id?email=diegosalcovsky@gmail.com&device_id=1&secret=ABE"`
This will return "Invalid request". Note that changing any of the three parameters will return the same result as the
request will fail to validate the user to the project and hence to the device that the history is being requested for.


Code review information + improvements

This flask application is meant to satisfy the requirements listed in 
https://memfault.notion.site/Memfault-Take-Home-Backend-Engineer-dddd26d8b34440ffbd277eedd4ab99fb

I want to list a few things that the project is missing and should be improved if this ever were meant for production:
These were intentionally omitted in my work due to time constraints.

1. There are no unit tests! We should use a library such as PyTest and build good unit testing. This is particularly 
important in a greenfield project in which we can aim to have full unit test coverage.
2. The database has bad security! There are no username / password for the app itself with restricted grants. The secrets
are saved in the database in plain text which is also awful. The secrets should be encrypted.

Functionality that could be added
1. Make sure devices are upgrading to the latest available version
2. Prevent devices from logging an upgrade event more than once
3. Provide the ability to ask a device which version they are on
4. Provide the ability to push a rollback if a version is found to have a critical bug


Tech used
1. Postgres - chosen because I have a lot of experience working with it and it is open source. It's a relational database
which is perfect for the problem we are trying to solve in this assignment and in line with the proposed database in the 
requirements.
2. Poetry - poetry is a dependency management tool. It creates a virtual environment specific to
the project and generates a pyproject.toml file. It installs and builds python packages. I don't have much experience 
using this tool, but it's been very easy to learn and use. 
3. Alembic - is a database migration tool. I wanted to be able to build the baseline outlined in the requirements and 
then make and track any changes I wished to make. I found alembic to be a great tool as it will automatically create my
migrations scripts based on the SQLAlchemy models I build. Makes my life real easy. I have no professional experience with
alembic, but again it's been very easy to learn and use. (Developed by same people that developed SQLAlchemy)
4. SQLAlchemy - ORM. I didn't want to write SQL string and I have a lot of experience working with SQLAlchemy. That being
said, writing queries can be a little more verbose than I would like.
5. Flask - We need a web framework to make sending HTTP requests easy. I have a lot of experience with flask, so I chose
to use it over Django.

I think I didn't miss any significant libraries. I'm happy to have further conversations about my choices!


Final requirement - 1m devices

I have not made any specific architectural decisions to cover this requirement. Ultimately I think this would be best
handled scaling horizontally our servers. Granted there are no bugs in my code that would make the service particularly 
poor performing. I will note that in the past I've had experiences in which using python and an ORM were not the most
performant choices and refactors had to be made. But ultimately I think it's too soon in this project's life to make such
determinations :-)