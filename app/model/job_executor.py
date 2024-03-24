from abc import ABC, abstractmethod
from utils.simple_logger import SimpleLogger

class JobExecutor(ABC):
    def __init__(self):
        self.logger = SimpleLogger()
        pass

    @abstractmethod
    def get_model(self):
        return self.model

    @abstractmethod
    def execute(self):
        pass
