"""Module for the Job Class and dependencies."""

import datetime

from enum import Enum


class SerializableEnum(Enum):
    """Class used to serialize Enum values."""

    def serialize(self):
        """Serializes self by return its value."""
        return self.value


class Status(SerializableEnum):
    """Enum with the status of Job requests."""

    PROCESSING = "PROCESSING"
    PROCESSED_OK = "PROCESSED_OK"
    PROCESSED_ERROR = "PROCESSED_ERROR"


class ResultType(SerializableEnum):
    """Enum witg the Types of restults that each model can provide."""

    TEXT = "TEXT"
    IMAGE = "IMAGE"


class Job:
    """Represents a inference request for a specific model."""

    @staticmethod
    def from_json(json):
        """Creates a Job from a Json string."""
        return Job(json["prompt"], Status.PROCESSING, json["model"])

    def __init__(
        self,
        prompt: str,
        status: str,
        model: str,
        result: str = None,
        result_type: str = None,
        job_id: int = None,
        timestamp: datetime = None,
    ):
        self.prompt = prompt
        self.status = Status(status)
        self.model = model
        self.job_id = job_id
        self.result = result
        self.result_type = ResultType(result_type) if result_type is not None else None
        self.timestamp = timestamp or datetime.datetime.now()

    def to_json(self):
        """Converts current object to a Json string."""
        json = {
            "id": self.job_id,
            "prompt": self.prompt,
            "status": self.status.serialize(),
            "model": self.model,
            "timestamp": self.timestamp.isoformat(),
        }

        if self.result is not None:
            json["result"] = self.result

        if self.result_type is not None:
            json["result_type"] = self.result_type.serialize()

        return json

    def __repr__(self):
        return f"""Job(
            id={self.job_id}
            , prompt='{self.prompt}'
            , status='{self.status}'
            , model='{self.model}'
            , result_type='{self.result_type}'
            , timestamp={self.timestamp})"""
