import datetime
from enum import Enum

class SerializableEnum(Enum):
    def serialize(self):
        return self.value

class Status(SerializableEnum):
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"

    def serialize(self):
        return self.value


class SerializableEnum(Enum):
    def serialize(self):
        return self.value


class ResultType(SerializableEnum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"

    def serialize(self):
        return self.value


class Job:

    @staticmethod
    def from_json(json):
        return Job(json['prompt'], Status.PROCESSING, json['model'])
    
    def __init__(self, prompt:str, status:str, model:str, result:str=None, result_type:str=None, id:int=None, timestamp:datetime=None):
        self.prompt = prompt
        self.status = Status(status)
        self.model = model
        self.id = id
        self.result = result
        self.result_type = ResultType(result_type) if result_type is not None else None
        self.timestamp = timestamp or datetime.datetime.now()
    
    def to_json(self):
        json = {
            "id": self.id,
            "prompt": self.prompt,
            "status": self.status.serialize(),
            "model": self.model,
            "timestamp": self.timestamp.isoformat()
        }

        if (self.result is not None):
            json["result"] = self.result
                    
        if (self.result_type is not None):
            json["result_type"] = self.result_type.serialize()

        return json
    
    def __repr__(self):
        return f"Job(id={self.id}, prompt='{self.prompt}', status='{self.status}', model='{self.model}', result='{self.result}', result_type='{self.result_type}' timestamp={self.timestamp})"
