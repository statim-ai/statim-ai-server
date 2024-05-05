# statim-ai-server-base

## What is this?

--TODO--

## Progress

A list of tasks yet to be implemented and the ones already implemented.

### TODO
- Convert "model" to "model_id"
- Make uniform use of Model ID name

- Add support for errors while doing inference

- Add glossary to README: Handler, Model, Job, etc.
- Add REST requests to /docs
- Add swagger
- Add input validation
- Test saving sqlite file locally to keep state

- Add start processing date
- Add end processing date
- Add API Keys support
- Add audit logging to database
- Add API to access images directly?
- Send images on job endpoint?
- Add limit and offset to job entpoint
- Add arch image to README
- Improve the model download to avoid copying extra files (this avoids extra model downloads when no other file changes are made)
- Add docker-compose support
- Init vs start syntaxt
- Add multi-stage support to Dockerfile?
- Disable outgoing connections on the container
- Add status message to job
- Updated logger format to add method to class name inside [...]

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
- Get version from pyproject file to build the docker image
- First published image on Docker Hub
- Add tests
- Add error message if no model is loaded
- Update repo and README to the new statim-ai-server-base vision