"""Class to handle inference requests."""

# ⚠️⚠️⚠️ WARNING ⚠️⚠️⚠️
# This is a example file

from model.base_job_handler import BaseJobHandler, ResultType
from model.job import Job

from . import create_model

MODEL_ID = "Writer/palmyra-small"


class JobHandler(BaseJobHandler):
    """Class to handle inference requests."""

    def __init__(self):
        super().__init__()
        self.logger.info(f"[{MODEL_ID}] init")

        # Init the model
        self.tokenizer, self.model = create_model.create_model()

    def get_model(self) -> str:
        """Returns the Model ID that this Handler handles."""
        return MODEL_ID

    def get_result_type(self) -> ResultType:
        """Returns the type of resource that this Handler produces."""
        return ResultType.TEXT

    def execute(self, job: Job) -> str:
        """
        Run the inference step and convertion to string.
        It is this Class responsiblity to return a string object
        that will be saved on the database.
        """
        self.logger.info(f"[{MODEL_ID}] execute")

        input_ids = self.tokenizer(job.prompt, return_tensors="pt").input_ids
        outputs = self.model.generate(input_ids)

        return self.tokenizer.decode(outputs[0])
