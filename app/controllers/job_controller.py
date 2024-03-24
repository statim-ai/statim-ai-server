from flask import Blueprint, jsonify, request
from flasgger import swag_from
from manager.job_manager import JobManager
from utils.simple_logger import SimpleLogger
from repository.job_repository import JobRepository
from model.job import Job

# Init logger
logger = SimpleLogger()

# Get Job Manager
job_manager = JobManager()

# Init jobs repository
job_repository = JobRepository()

# Init jobs blueprint
job_blueprint = Blueprint('job', __name__)


#@swag_from('colors.yml')
@job_blueprint.route('/job/', methods=['GET'])
def get_jobs():
    logger.info('GET /job')

    # Get all jobs from database
    jobs = job_repository.get_all()

    jobs_json = []
    for job in jobs:
        jobs_json.append(job.to_json())
        
    return jsonify(jobs_json)


#@swag_from('colors.yml')
@job_blueprint.route('/job/<int:job_id>', methods=['GET'])
def get_job(job_id):
    logger.info(f"GET /job/{job_id}")

    # Get job from database
    job = job_repository.get_by_id(job_id)

    if job is None:
        return jsonify(), 404
    
    logger.info(f"Returning {job}")

    return jsonify(job.to_json())


#@swag_from('colors.yml')
@job_blueprint.route('/job', methods=['POST'])
def add_job():
    logger.info(f"POST /job {request.json}")
    
    job = Job.from_json(request.json)
    logger.info(f"Processing {job}")

    # Insert job in database
    job = job_repository.create_job(job)

    # Add job to job manager
    job_manager.add(job)

    return jsonify(job.to_json()), 200
