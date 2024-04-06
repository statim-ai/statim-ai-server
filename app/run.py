import signal
import sys
from flask import Flask
from waitress import serve
from flasgger import Swagger
from controllers import job_controller, model_controller
from manager.job_manager import JobManager


swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger_template = {
  "swagger": "2.0",
  "info": {
    "title": "My API",
    "description": "API for my data",
    "contact": {
      "responsibleOrganization": "ME",
      "responsibleDeveloper": "Me",
      "email": "me@me.com",
      "url": "www.me.com",
    },
    "version": "0.0.1"
  },
  "host": "mysite.com",  # overrides localhost:500
  "basePath": "/",  # base bash for blueprint registration
  "schemes": [
    "http"
  ],
  "operationId": "getmyData"
}


def main():
  # Set the signal handler
  signal.signal(signal.SIGINT, signal_handler)

  # Init Job Manager
  job_manager = JobManager()
  job_manager.start()

  # Init Flask app
  app = Flask(__name__)

  # Register controlers
  app.register_blueprint(job_controller.job_blueprint)
  app.register_blueprint(model_controller.model_blueprint)

  # Init swagger
  swagger = Swagger(app, config=swagger_config, template=swagger_template)

  # Init waitress server
  serve(app, host="0.0.0.0", port=5000)


def signal_handler(sig, frame):
    print('SIGINT, exiting...')
    sys.exit(0)


main()
