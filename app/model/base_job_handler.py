from abc import ABC, abstractmethod

from utils.simple_logger import SimpleLogger

from model.job import ResultType


class BaseJobHandler(ABC):
    def __init__(self):
        self.logger = SimpleLogger()
        pass

    @abstractmethod
    def get_model(self) -> str:
        return self.model

    @abstractmethod
    def get_result_type(self) -> ResultType:
        return self.result_type

    @abstractmethod
    def execute(self) -> str:
        pass
