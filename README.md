# SID-api
API and database management for "Sistema de Informações sobre Dengue" (SID).
 
This project is developed for PCS3643 (Laboratório de Engenharia de Software).

Developed by:
- [Erick Sousa](https://github.com/Erick-DAS)
- [Carlos Engler](https://github.com/henriqueedu2001)
- [Henrique Eduardo](https://github.com/henriqueedu2001)
- [Enzo Tassini](https://github.com/Enzo-Tssn)

Read the following sections in order to start developing.

## Install main Dependencies

- Python 3.8+
- Poetry
- docker-compose
- make

## Setup environment variables

First of all, create a `.env` file sampled as the example `sample.env`, setting values for database credentials and other important variables.

*Note: All the variables set there must be added to `app.core.config` to be accessed globally by the code.*

## Setup environment dependencies

- Create the poetry isolated virtual environment
`make start-venv`
- Install dependencies
`make install`

## Run database

Run `make run-db`

## Migrate database version

Run `make migrate`

## Run the API

Run `make run-api`

Now that the API is running, one can access `http://localhost:8000/docs` to access the endpoints and documentation with swagger.





