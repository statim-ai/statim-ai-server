"""Module with the abstract class to handle inference requests."""

from abc import ABC, abstractmethod

from utils.simple_logger import SimpleLogger

from model.job import ResultType


class BaseJobHandler(ABC):
    """Abstract class to handle inference requests."""

    def __init__(self):
        self.logger = SimpleLogger()
        pass

    @abstractmethod
    def get_model(self) -> str:
        """Returns the Model ID that this Handler handles."""
        return self.model

    @abstractmethod
    def get_result_type(self) -> ResultType:
        """Returns the type of resource that this Handler produces."""
        return self.result_type

    @abstractmethod
    def execute(self) -> str:
        """
        Run the inference step and convertion to string.
        It is this Class responsiblity to return a string object
        that will be saved on the database.
        """
        pass
