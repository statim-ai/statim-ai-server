import datetime
import json
from enum import Enum

class SerializableEnum(Enum):
    def serialize(self):
        return self.value

class Status(SerializableEnum):
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"

    def serialize(self):
        return self.value

class Job:

    @staticmethod
    def from_json(json):
        return Job(json['text'], Status.PROCESSING, json['model'])
    
    def __init__(self, text:str, status:str, model:str, id:int=None, timestamp:datetime=None):
        self.text = text
        self.status = Status(status)
        self.model = model
        self.id = id
        self.timestamp = timestamp or datetime.datetime.now()
    
    def to_json(self):
        return {
            "id": self.id,
            "text": self.text,
            "status": self.status.serialize(),
            "model": self.model,
            "timestamp": self.timestamp.isoformat()
        }
    
    def __repr__(self):
        return f"Job(id={self.id}, text='{self.text}', status='{self.status}', model='{self.model}', timestamp={self.timestamp})"
