## Cache Api Application

The main proposal of this project is to study the main concepts of an architecture the gets data from a generic source and ingests it on a cache structure.

For this project the stack is:
- FastAPI
- Redis

The data for this project is from https://fakerapi.it/en.

### The basic architecture is:
![Project architecture](/.github/Cache-Api-App-Architecture.png)

### About services:

#### Redis and Redisinsight 

The Redis stack runs from a docker environment.

-Redis port: 6379
-Redisinsight port: 8001

#### FastAPI

It was decide to run locally, installing in a virtual environment along with the other Python's dependencies (requirements.txt file).

## Run Application

### Project Structure

![Project directories structure](https://github.com/bereoff/cache-api-application/blob/main/project_directory_structure.png)

To run this project as it was concepted, is it necessary to previosly install Docker and Docker Compose (more info: [Docker](https://docs.docker.com/engine/install/)).

### Steps
* Start/Run Redis Docker services: docker-compose up (After docker and docker compose installed) to pull (if you don't have any Redis/Redisinsight local image).
  
* Create a virtual environment: There are many possibilities to create a Python virtual environment, but I will use the built-in Python way:
  - In your root project folder (./cache-data-app):
    - python3 -m venv <env_name>
  - Depends on what OS you are using, will need a different way to activate you python virtual environt, in my case it's an OS  based on Linux.
    - source <env_name>/bin/activate
  - Install requirements (after a virtual environment activated):
    - python3 -m pip install -r requirements.txt

After the previous steps concluded, is time to run the uvicorn server (all this flow is based on a development environment approach). For a production environment, others steps are necessary to give a more robustness and security when you will deploy the project in a cloud/on premisse server.

After this disclaimer, to start the server properly is necessary to run this command:
- uvicorn app:app --host=localhost --port=8000 --reload

Now, and if the previous steps were concluded without errors, if you access the urls:
-http://localhost:8001/ [Redisinsight UI]
-http://localhost:8000/docs [FastAPI swagger]












