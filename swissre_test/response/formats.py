import enum
import json
from dataclasses import asdict
from abc import ABC, abstractmethod
import typing
from swissre_test.entities import ResponseEntity


class ResponseFormat(ABC):
    @abstractmethod
    async def render(self, entities: typing.List[ResponseEntity]) -> str:
        raise NotImplementedError


class JsonFormat(ResponseFormat):
    async def render(self, entities: typing.List[ResponseEntity]) -> str:
        return json.dumps([asdict(entity) for entity in entities])


@enum.unique
class Format(str, enum.Enum):
    json = 'json'

    def get_object(self):
        return {
            Format.json.name: JsonFormat
        }[self.name]()
