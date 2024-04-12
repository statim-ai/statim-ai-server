import base64
import io
from model.job import Job
from model.base_job_handler import BaseJobHandler, ResultType
from . import create_model


class JobHandler(BaseJobHandler):

    def __init__(self):
        super().__init__()
        self.logger.info("[stabilityai/sdxl-turbo] init")
        self.pipe = create_model.create_model()


    def get_model(self):
        return "stabilityai/sdxl-turbo"


    def get_result_type(self) -> ResultType:
        return ResultType.IMAGE


    def execute(self, job:Job) -> str:
        self.logger.info("[stabilityai/sdxl-turbo] execute")

        image = self.pipe(prompt=job.prompt, num_inference_steps=1, guidance_scale=0.0).images[0]

        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        base64str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return f'data:image/png;base64,{base64str}'
