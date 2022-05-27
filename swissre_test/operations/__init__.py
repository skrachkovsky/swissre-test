from abc import abstractmethod
import enum
import typing

if typing.TYPE_CHECKING:
    from ..readers import DataReader
    from ..entities import EntityFactory


class Operation:
    def __init__(self, reader: 'DataReader', entity_factory: 'EntityFactory', **kwargs) -> None:
        self._reader = reader
        self._entity_factory = entity_factory

    @abstractmethod
    async def _perform(self):
        raise NotImplementedError

    async def execute(self):
        return await self._perform()


@enum.unique
class OperationAlias(str, enum.Enum):
    """
    Operations:
        mfi - Most frequent IP.
        fli - Least frequent IP.
        eps - Events per second.
        epm - Events per minute.
        taobe - Total amount of bytes exchanged.
    """

    most_frequent_ip = 'mfi'
    least_frequent_ip = 'fli'
    events_per_second = 'eps'
    events_per_minute = 'epm'
    total_amout_of_bytes_exchanged = 'taobe'
