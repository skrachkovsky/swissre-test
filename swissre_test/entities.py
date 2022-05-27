import typing
from abc import abstractmethod
from dataclasses import dataclass


@dataclass
class DataEntity:
    timestamp: float
    ip: str
    bytes_number: int


class EntityFactory:
    @abstractmethod
    def str_to_entity(self, data: str) -> 'DataEntity':
        raise NotImplementedError


@dataclass
class ResponseError:
    label: str
    details: str


@dataclass
class ResponseEntity:
    timestamp: float
    operation: str
    result: typing.Any
    error: typing.Optional[ResponseError]
