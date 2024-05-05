"""Module for the JobManager class."""

import base64
import io
import os

from importlib import import_module
from threading import Thread

from PIL import Image
from model.job import Job, ResultType, Status
from repository.job_repository import JobRepository
from utils.simple_logger import SimpleLogger
from utils.simple_queue import SimpleQueue
from utils.utils import get_directories_from_path

HANDLERS_PATH = f"{os.getcwd()}/app/handlers"
HANDLER_MODULE = "handlers.{}.job_handler"
HANDLER_CLASS_NAME = "JobHandler"


class JobManager:
    """Manager class to manage Jobs requests."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Construtor that implements the Singleton pattern and
        dynamically loads all available handlers.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

            cls._instance.logger = SimpleLogger()
            cls._instance.queue = SimpleQueue()
            cls._instance.job_repository = JobRepository()

            # Search dynamically for handlers
            cls._instance.handlers = {}

            for directory in get_directories_from_path(HANDLERS_PATH):
                job_handler_class = getattr(import_module(HANDLER_MODULE.format(directory)), HANDLER_CLASS_NAME)

                # Create new handler instance
                job_handler_instance = job_handler_class()
                model_id = job_handler_instance.get_model()

                if model_id in cls._instance.handlers.keys():
                    raise Exception(f"A Handler with the model_id '{model_id}' is already registered")

                cls._instance.handlers[model_id] = job_handler_instance

            # Check if no Handlers are registered
            if len(cls._instance.handlers) == 0:
                cls._instance.logger.error(
                    "[JobManager.start] Zero handlers registered, to learn how to add one visit: https://github.com/statim-ai/statim-ai-server-example-text-model"
                )

        return cls._instance

    def start(self) -> None:
        """Start the background progress to process Jobs."""
        # Print registered Handlers
        for key in self.handlers.keys():
            self.logger.info(f"[JobManager.start] Registered handler: {key}")

        def job_listener() -> None:
            while True:
                try:
                    job = self.queue.dequeue()
                    self.logger.info(f"[JobManager.job_listener] Job to process: {job}")

                    if job.model in self.handlers:
                        # Get hander
                        handler = self.handlers[job.model]

                        # Execute job
                        result = handler.execute(job)
                        result_type = handler.get_result_type()

                        # Convert result to specific object
                        if result_type == ResultType.TEXT:
                            # Handle str results
                            if isinstance(result, str):
                                job.result = result
                                job.result_type = ResultType.TEXT
                                job.status = Status.PROCESSED_OK
                            else:
                                raise Exception(f"Text Model is not returning a string: {type(result)}")

                        elif result_type == ResultType.IMAGE:
                            # Handle PIL Image objects
                            if isinstance(result, Image.Image):
                                buffer = io.BytesIO()
                                result.save(buffer, format="PNG")
                                base64str = base64.b64encode(buffer.getvalue()).decode("utf-8")

                                job.result = f"data:image/png;base64,{base64str}"
                                job.result_type = ResultType.IMAGE
                                job.status = Status.PROCESSED_OK
                            else:
                                raise Exception(f"Image Model is not returning an Image: {type(result)}")

                        else:
                            # Model is not registered with a know type
                            raise Exception(f"Model is not registered with a know type: {result_type}")
                    else:
                        # No model handler found for model
                        raise Exception(f"No Handler found for Model: {job.model}")

                except Exception as e:
                    self.logger.error(f"[JobManager.job_listener] Exception processing request: {str(e)}")

                    # Set job status to processed with error
                    job.status = Status.PROCESSED_ERROR
                    job.result_type = None
                finally:
                    # Always update the Job entry
                    self.job_repository.update_job(job)

        thread = Thread(target=job_listener, daemon=True)
        thread.start()

        self.logger.info("[JobManager.start] Ready!")

    def add(self, job: Job) -> None:
        """Add job to queue to be processed."""
        self.queue.enqueue(job)

    def get_handlers(self):
        """Returns a list of available handlers."""
        return self.handlers.values()
