"""Class to handle inference requests."""

# ⚠️⚠️⚠️ WARNING ⚠️⚠️⚠️
# This is a example file

import base64
import io

from model.base_job_handler import BaseJobHandler, ResultType
from model.job import Job

from . import create_model

MODEL_ID = "stabilityai/sdxl-turbo"


class JobHandler(BaseJobHandler):
    """Class to handle inference requests."""

    def __init__(self):
        super().__init__()
        self.logger.info(f"[{MODEL_ID}] init")

        # Init the model
        self.pipe = create_model.create_model()

    def get_model(self):
        """Returns the Model ID that this Handler handles."""
        return MODEL_ID

    def get_result_type(self) -> ResultType:
        """Returns the type of resource that this Handler produces."""
        return ResultType.IMAGE

    def execute(self, job: Job) -> str:
        """
        Run the inference step and convertion to string.
        It is this Class responsiblity to return a string object
        that will be saved on the database.
        """
        self.logger.info(f"[{MODEL_ID}] execute")

        image = self.pipe(
            prompt=job.prompt, num_inference_steps=1, guidance_scale=0.0
        ).images[0]

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        base64str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return f"data:image/png;base64,{base64str}"
