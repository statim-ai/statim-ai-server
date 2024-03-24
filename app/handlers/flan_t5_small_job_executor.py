from model.job import Job
from model.job_executor import JobExecutor
from . import flan_t5_small_create_model


class FLANT5SmallJobExecutor(JobExecutor):

    def __init__(self):
        super().__init__()
        self.logger.info("[FLANT5SmallJobExecutor] init")

        self.tokenizer, self.model = flan_t5_small_create_model.create_model()


    def get_model(self):
        return "google/flan-t5-small"


    def execute(self, job:Job) -> str:
        self.logger.info("[FLANT5SmallJobExecutor] execute")

        input_text = "translate English to German: How old are you?"
        input_ids = self.tokenizer(input_text, return_tensors="pt").input_ids

        outputs = self.model.generate(input_ids)
        print(self.tokenizer.decode(outputs[0]))
        
        return ''