import typing
from swissre_test.operations.events_num import EventsPerMinute, EventsPerSecond

from swissre_test.operations.total_bytes import TotalAmoutOfBytesExchanged

from .ip_frequecny import LastFrequentIp, MostFrequentIp

if typing.TYPE_CHECKING:
    from ..readers import DataReader
    from ..entities import EntityFactory


class Operations:
    async def most_frequent_ip(self, reader: 'DataReader', entity_factory: 'EntityFactory'):
        return await MostFrequentIp(reader, entity_factory).execute()

    async def least_frequent_ip(self, reader: 'DataReader', entity_factory: 'EntityFactory'):
        return await LastFrequentIp(reader, entity_factory).execute()

    async def events_per_second(self, reader: 'DataReader', entity_factory: 'EntityFactory'):
        return await EventsPerSecond(reader, entity_factory).execute()

    async def events_per_minute(self, reader: 'DataReader', entity_factory: 'EntityFactory'):
        return await EventsPerMinute(reader, entity_factory).execute()

    async def total_amout_of_bytes_exchanged(self, reader: 'DataReader', entity_factory: 'EntityFactory'):
        return await TotalAmoutOfBytesExchanged(reader, entity_factory).execute()
