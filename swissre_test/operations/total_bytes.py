from . import Operation


class TotalAmoutOfBytesExchanged(Operation):
    async def _perform(self):
        _res = 0
        async for line in self._reader.read():
            item = self._entity_factory.str_to_entity(line)
            _res += item.bytes_number
        return _res
