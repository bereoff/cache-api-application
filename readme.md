## Cache Api Application

The proposal of this project is to demonstrate the main concepts of an architecture the gets data from a generic source and ingests it on a cache structure.

For this project the stack is:
- [FastAPI](https://fastapi.tiangolo.com/)
- [Redis](https://redis.io/docs/getting-started/)

The data for the project are from https://fakerapi.it/en.

> ### The basic architecture is:

![Project architecture](https://github.com/bereoff/cache-api-application/blob/main/Cache-Api-App-Architecture.png)

> ### About the services:

#### Redis and Redisinsight 

The Redis stack runs from a docker environment.

- Redis port: 6379
- Redisinsight port: 8001

#### FastAPI

FastAPI runs locally, from a virtual environment along with the other Python's dependencies (requirements.txt file).

## Run Application

> ### Project Structure

<p align="center">
  <img src="https://github.com/bereoff/cache-api-application/blob/main/project_directory_structure.png" />
</p>


To run this project as it was concepted, it is necessary previosly to install Docker and Docker Compose (more info: [Docker](https://docs.docker.com/engine/install/)).

> ### Steps
* Start/Run Redis Docker services: docker-compose up (After docker and docker compose installed) to pull (if you don't have any Redis/Redisinsight local image) Redis and Redisinsight images and start the containers from the services.
  
* Create a virtual environment: There are many possibilities to create a Python virtual environment, but I will use the built-in Python way:
  - In your project root folder (./cache-data-app):
    ```
      python3 -m venv .venv
    ```
  - Depending on what OS you are using, you will need a different way to activate your python virtual environment. In my case it's a Linux OS.
    ```
      source <env_name>/bin/activate
    ```
  - Install requirements (after a virtual environment activated):
    ```
      python3 -m pip install -r requirements.txt
    ```
After the previous steps concluded, is time to run the uvicorn server (all this flow is based on a development environment approach). For a production environment, others steps are necessary to give a more robustness and security when you will deploy the project in a cloud/on-premise server.

After this consideration, to start the server properly is necessary to run this command in the same level as app.py file (inside cache-app folde):
```
  uvicorn main:app --host=localhost --port=8000 --reload
```

Now, and if the previous steps were concluded without errors, if you access the follow urls, you will get the service UIs:
```
  http://localhost:8001/ [Redisinsight UI]
  http://localhost:8000/docs [FastAPI swagger]
```












