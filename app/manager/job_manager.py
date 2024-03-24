from threading import Thread
from utils.simple_queue import SimpleQueue
from utils.simple_logger import SimpleLogger
from model.job import Job, Status
from repository.job_repository import JobRepository
from handlers.sdxl_job_executor import SDXLJobExecutor
from handlers.flan_t5_small_job_executor import FLANT5SmallJobExecutor

class JobManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.logger = SimpleLogger()
            cls._instance.queue = SimpleQueue()
            cls._instance.job_repository = JobRepository()

            # Register Executors
            cls._instance.executors = {}

            #executor1 = SDXLJobExecutor()
            #cls._instance.executors[executor1.get_model()] = executor1

            executor2 = FLANT5SmallJobExecutor()
            cls._instance.executors[executor2.get_model()] = executor2
            
        return cls._instance
    

    def start(self) -> None:
        self.logger.info('[JobManager] start')

        # Print registered executors
        for key in self.executors.keys():
            self.logger.info(f'[JobManager] start - registered executor: {key}')
        
        def job_listener() -> None:
            while (True):
                job = self.queue.dequeue()
                self.logger.info(f'[JobManager] job_listener - job to process: {job}')

                if job.model in self.executors:
                    # Execute job
                    payload = self.executors[job.model].execute(job)
                    
                    # TODO Add payload to job
                else:
                    # No model executor found for model
                    self.logger.info(f'[JobManager] job_listener - no executor found for model: {job.model}')
                
                # Update database status
                job.status = Status.PROCESSED
                self.job_repository.update_job(job)

        thread = Thread(target = job_listener, daemon=True)
        thread.start()


    def add(self, job:Job) -> None:
        # Add job to queue
        self.queue.enqueue(job)