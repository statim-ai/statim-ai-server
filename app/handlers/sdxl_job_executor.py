from model.job import Job
from model.job_executor import JobExecutor
from . import sdxl_create_model


class SDXLJobExecutor(JobExecutor):

    def __init__(self):
        super().__init__()
        self.logger.info("[SDXLJobExecutor] init")
        self.pipe = sdxl_create_model.create_model()


    def get_model(self):
        return "stabilityai/sdxl-turbo"


    def execute(self, job:Job) -> str:
        self.logger.info("[SDXLJobExecutor] execute")
        image = self.pipe(prompt=job.text, num_inference_steps=1, guidance_scale=0.0).images[0]

        # Return image
        
        return ''