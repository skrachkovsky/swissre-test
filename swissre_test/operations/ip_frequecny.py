from . import Operation


class MostFrequentIp(Operation):
    async def _perform(self):
        _ips = {}
        _max_n = 0
        _max_ip = ''
        async for line in self._reader.read():
            item = self._entity_factory.str_to_entity(line)
            if item.ip not in _ips:
                _ips[item.ip] = 1
            else:
                _ips[item.ip] += 1
            if item.ip == _max_ip:
                _max_n = _ips[item.ip]
            elif _ips[item.ip] > _max_n:
                _max_n = _ips[item.ip]
                _max_ip = item.ip
        return _max_ip


class LastFrequentIp(Operation):
    async def _perform(self):
        _ips = {}
        _min_n = float('inf')
        _min_ip = ''
        async for line in self._reader.read():
            item = self._entity_factory.str_to_entity(line)
            if item.ip not in _ips:
                _ips[item.ip] = 1
            else:
                _ips[item.ip] += 1
            if item.ip == _min_ip:
                _min_n = _ips[item.ip]
            elif _ips[item.ip] < _min_n:
                _min_n = _ips[item.ip]
                _min_ip = item.ip
        return _min_ip
