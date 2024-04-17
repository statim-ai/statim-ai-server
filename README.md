# statim-ai-server

## What is statim-ai-server?

Nowdays it is easy to run AI models (for inference) locally or on the cloud without much effort.

`statim-ai-server` wants to provide a out-of-box experience running those models locally or on infrastructure without being tied to specific providers and providing quality-of-life features.

## What does it provides?

This repo generate a Docker image ready to use with built-in(s) LLM model(s) and a couple of usefull features:

- Job oriented, asynchronous, HTTP REST API
- SQLite database to store metadata about each request
- Support for multiple LLM models on the same instance
- After the image creation no more downloads are needed
- Easy to add new LLM models
- Logging

## How it works?

The target artifact of this repository is a Docker image, ready to be integrated as a REST API service.

When the service starts one or more LLM models are loaded into memory and the REST API allows the user to make requests to the loaded models.

All the requests are saved into a SQLite database that can be queried later.

This repository already have support for a couple of models out-of-box as example but the main goal is to be used as a template for other models that would be usefull for the user specific case.

## How to Run?

1. Clone the repo:
```sh
# The repo is ready for build after clone, except creating a `.env` file (step 2)
git clone git@github.com:statim-ai/statim-ai-server.git
```

2. Create a `.env` file:
```sh
# For now you can just use the template, no changes needed
cp .env.template .env
```

3. Install and start Docker. Note: the server might use a lot of memory (it is dependent on the models loaded), you might need to adjust the memory available to your containers.
```sh
# To check if docker is running use:
docker ps
```

4. Create the docker image:
```sh
# This will crate new docker image: statim-ai-server
make build
```

5. Run the docker image:
```sh
# This will run the statim-ai-server docker image
make run
```

6. Make a request to the server:
```sh
curl --request POST \
    --url http://0.0.0.0:5000/job \
    --header 'Content-Type: application/json' \
    --data '{
        "prompt": "A cat in space",
        "model": "stabilityai/sdxl-turbo"
    }'
```

7. Get a response from the server:
```json
{
	"id": 1,
	"model": "stabilityai/sdxl-turbo",
	"prompt": "A cat in space",
	"status": "PROCESSING",
	"timestamp": "2024-04-07T15:22:05.813912"
}
```

8.  Pool the server until the request is processed:
```sh
curl --request GET \
    --url http://0.0.0.0:5000/job/1
```

## How to add a new model?

...

## Beware of the model licenses

The LLMs used by this project might have a license that doesn't allow commercial or other kinds of usage.

Before using this server in a specific enviroment make sure that the use case is allowed by the LLM license.

## Progress

A list of tasks yet to be implemented and the ones already implemented.

### TODO
- Add support for errors while doing inference
- Convert "model" to "model_id"
- Add glossary to README: Handler, Model, Job, etc.
- Add status message to job
- Updated logger format to add method to class name inside [...]
- Add API Keys support
- Add audit logging
- Add start processing date
- Add end processing date
- Add swagger
- Add API to access images directly?
- Send images on job endpoint?
- Add limit and offset to job entpoint
- Save sqlite file locally to keep state
- Add input validation
- Add arch image to README
- Add REST requests to /docs
- Improve the model download to avoid copying extra files (this avoids extra model downloads when no other file changes are made)
- Make uniform use of Model ID name
- Tests
- Add docker-compose support
- Version file
- Init vs start syntaxt
- Add multi-stage support to Dockerfile?
- Disable outgoing connections on the container
- Use docker squash?
- Generate docker image with version from poetry

### DONE
- Create statim-ai-server repo
- Add .gitignore
- Initial commit
- Load handlers in a dynamically
- Group handlers in folder
- Rename Executor to handler
- Rename "text" to prompt
- Add column to store result on DB
- Get available models API
- Fix docker user (myuser)
- Use poetry instead of requirements
- Fix docker image name (my-python-app)
- Test multimodel
- License file
- Which part of the code should be responsbile for serializing the model output? Generic on the Job Manager?
- Save images on the database in base64
- Create .env file
- Add ruff
- Validate if multiple handlers have the same name
- Which part of the code should be responsbile for serializing the model output? Generic on the Job Manager? Moved this code to JobManager
