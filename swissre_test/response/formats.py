import enum
import json
from dataclasses import asdict
from abc import ABC, abstractmethod
from swissre_test.entities import ResponseEntity


class ResponseFormat(ABC):
    @abstractmethod
    async def render(self, entity: ResponseEntity) -> str:
        raise NotImplementedError


class JsonFormat(ResponseFormat):
    async def render(self, entity: ResponseEntity) -> str:
        return json.dumps(asdict(entity))


@enum.unique
class Format(str, enum.Enum):
    json = 'json'

    def get_object(self):
        return {
            Format.json.name: JsonFormat
        }[self.name]()
