from collections import namedtuple
import re
from dataclasses import dataclass
from functools import cached_property

from .exceptions import ValidationError
from .provider import DataProvider
from .entities import DataEntity, EntityFactory


@dataclass
class SquidEntity(DataEntity):
    header_bytes: int


class SquidEntityFactory(EntityFactory):
    @cached_property
    def _re_pattern(self):
        return re.compile(r'\s+')

    @cached_property
    def _nt(self):
        return namedtuple('SquidEntityTuple', ('ip', 'timestamp', 'bytes_number', 'header_bytes'))

    def str_to_entity(self, data: str) -> 'SquidEntity':
        """
        Field 1: 1157689324.156 [Timestamp in seconds since the epoch]
        Field 2: 1372 [Response header size in bytes]
        Field 3: 10.105.21.199 [Client IP address]
        Field 4: TCP_MISS/200 [HTTP response code]
        Field 5: 399 [Response size in bytes]
        Field 6: GET [HTTP request method]
        Field 7: http://www.google-analytics.com/__utm.gif? [URL]
        Field 8: badeyek [Username]
        Field 9: DIRECT/66.102.9.147 [Type of access/destination IP address]
        Field 10: image/gif [Response type]
        """
        cols = self._re_pattern.split(data)
        try:
            """
            ❗❗❗

            Building dataclass or other object is quite expencive operation in that case,
            but we have to build solid architecture
            """
            return SquidEntity(
                timestamp=float(cols[0]),
                ip=cols[2],
                bytes_number=int(cols[4]) + int(cols[1]),
                header_bytes=int(cols[1])
            )
        except (TypeError, ValueError, IndexError) as err:
            raise ValidationError(f'Can\'t build entity from row "{data}": {str(err)}')


class SquidProvider(DataProvider):
    @cached_property
    def _entity_factory(self):
        return SquidEntityFactory()
