from model.job import Job
from model.base_job_handler import BaseJobHandler, ResultType
from . import create_model


class JobHandler(BaseJobHandler):

    def __init__(self):
        super().__init__()
        self.logger.info("[Writer/palmyra-small] init")

        self.tokenizer, self.model = create_model.create_model()


    def get_model(self):
        return "Writer/palmyra-small"


    def get_result_type(self) -> ResultType:
        return ResultType.TEXT


    def execute(self, job:Job) -> str:
        self.logger.info("[Writer/palmyra-small] execute")

        input_ids = self.tokenizer(job.prompt, return_tensors="pt").input_ids
        outputs = self.model.generate(input_ids)
        
        return self.tokenizer.decode(outputs[0])