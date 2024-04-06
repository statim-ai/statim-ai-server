import os
from threading import Thread
from importlib import import_module
from utils.utils import get_directories_from_path
from utils.simple_queue import SimpleQueue
from utils.simple_logger import SimpleLogger
from model.job import Job, Status
from repository.job_repository import JobRepository

HANDLERS_PATH = f'{os.getcwd()}/app/handlers'
HANDLER_MODULE = 'handlers.{}.job_handler'
HANDLER_CLASS_NAME = 'JobHandler'

class JobManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            
            cls._instance.logger = SimpleLogger()
            cls._instance.queue = SimpleQueue()
            cls._instance.job_repository = JobRepository()
            
            # Search dynamically for handlers
            cls._instance.handlers = {}

            for directory in get_directories_from_path(HANDLERS_PATH):
                JobHandler = getattr(import_module(HANDLER_MODULE.format(directory)), HANDLER_CLASS_NAME)

                # Create new handler instance
                job_handler_instance = JobHandler()
                cls._instance.handlers[job_handler_instance.get_model()] = job_handler_instance

        return cls._instance
    

    def start(self) -> None:
        self.logger.info('[JobManager] start')

        # Print registered Handlers
        for key in self.handlers.keys():
            self.logger.info(f'[JobManager] start - registered handler: {key}')
        
        def job_listener() -> None:
            while (True):
                job = self.queue.dequeue()
                self.logger.info(f'[JobManager] job_listener - job to process: {job}')

                if job.model in self.handlers:
                    # Get hander
                    handler = self.handlers[job.model]

                    # Execute job
                    result = handler.execute(job)

                    # TODO Convert response to correct type
                    job.result = result
                    job.result_type = handler.get_result_type()
                else:
                    # No model handler found for model
                    self.logger.info(f'[JobManager] job_listener - no handler found for model: {job.model}')
                
                # Update database status
                job.status = Status.PROCESSED
                self.job_repository.update_job(job)

        thread = Thread(target = job_listener, daemon=True)
        thread.start()


    def add(self, job:Job) -> None:
        # Add job to queue
        self.queue.enqueue(job)


    def get_handlers(self):
        return self.handlers.values()