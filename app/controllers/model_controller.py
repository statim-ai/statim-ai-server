"""Controler to process Model requests."""

from flask import Blueprint, jsonify
from manager.job_manager import JobManager
from utils.simple_logger import SimpleLogger

# Init logger
logger = SimpleLogger()

# Get Job Manager
job_manager = JobManager()

# Init jobs blueprint
model_blueprint = Blueprint("model", __name__)


# @swag_from('colors.yml')
@model_blueprint.route("/model/", methods=["GET"])
def get_jobs():
    """Returns all Models."""
    logger.info("GET /model")

    # Get all model handlers
    handlers = job_manager.get_handlers()

    models_json = []
    for handler in handlers:
        models_json.append(
            {
                "id": handler.get_model(),
                "result_type": handler.get_result_type().serialize(),
            }
        )

    return jsonify(models_json)
