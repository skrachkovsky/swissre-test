import typing
from functools import cached_property

from .operations import OperationAlias
from .operations.invoker import Operations
from .exceptions import BadOperation
from .entities import EntityFactory

if typing.TYPE_CHECKING:
    from .readers import DataReader
    from .config import Config


class DataProvider:
    @cached_property
    def _entity_factory(self):
        return EntityFactory()

    @cached_property
    def _operations(self) -> Operations:
        return Operations()

    async def process(self, operation_name: OperationAlias, reader: 'DataReader', config: 'Config') -> typing.Any:
        match operation_name:
            case OperationAlias.most_frequent_ip:
                return await self._operations.most_frequent_ip(reader, self._entity_factory)
            case OperationAlias.least_frequent_ip:
                return await self._operations.least_frequent_ip(reader, self._entity_factory)
            case OperationAlias.events_per_second:
                return await self._operations.events_per_second(reader, self._entity_factory)
            case OperationAlias.events_per_minute:
                return await self._operations.events_per_minute(reader, self._entity_factory)
            case OperationAlias.total_amout_of_bytes_exchanged:
                return await self._operations.total_amout_of_bytes_exchanged(reader, self._entity_factory)
        raise BadOperation(f'Operation "{operation_name}" is not provided')
