import pytest
import os
import re
import math
from swissre_test.operations.events_num import EpsResult

from swissre_test.squid import SquidProvider
from swissre_test.readers import StringReader
from swissre_test.operations import OperationAlias
from swissre_test.provider.factory import Provider


@pytest.mark.asyncio
async def test_most_frequent_ip(squid_log, config):
    logs = squid_log(100, 60)
    reader = StringReader(logs)
    provider = SquidProvider()
    conf = config(operations=[OperationAlias.most_frequent_ip], provider=Provider.squid)
    result = await provider.process(reader, conf)

    _ips = {}
    _max_n = 0
    _max_ip = ''
    _retempl = re.compile(r'\s+')
    for line in logs.split(os.linesep):
        if not line.strip():
            continue
        ip = _retempl.split(line)[2]
        if ip not in _ips:
            _ips[ip] = 1
        else:
            _ips[ip] += 1
        if ip == _max_ip:
            _max_n = _ips[ip]
        elif _ips[ip] > _max_n:
            _max_n = _ips[ip]
            _max_ip = ip

    assert result[0][1] == _max_ip


@pytest.mark.asyncio
async def test_least_frequent_ip(squid_log, config):
    logs = squid_log(100, 60)
    reader = StringReader(logs)
    provider = SquidProvider()
    conf = config(operations=[OperationAlias.least_frequent_ip], provider=Provider.squid)
    result = await provider.process(reader, conf)

    _ips = {}
    _min_n = float('inf')
    _min_ip = ''
    _retempl = re.compile(r'\s+')
    for line in logs.split(os.linesep):
        if not line.strip():
            continue
        ip = _retempl.split(line)[2]
        if ip not in _ips:
            _ips[ip] = 1
        else:
            _ips[ip] += 1
        if ip == _min_ip:
            _min_n = _ips[ip]
        elif _ips[ip] < _min_n:
            _min_n = _ips[ip]
            _min_ip = ip

    assert result[0][1] == _min_ip


@pytest.mark.asyncio
async def test_events_per_second(squid_log, config):
    logs = squid_log(100, 60)
    reader = StringReader(logs)
    provider = SquidProvider()
    conf = config(operations=[OperationAlias.events_per_second], provider=Provider.squid)
    result = await provider.process(reader, conf)

    assert isinstance(result[0][1], EpsResult)

    intervals = {}
    _retempl = re.compile(r'\s+')
    for line in logs.split(os.linesep):
        if not line.strip():
            continue
        ts = _retempl.split(line)[0]
        _intv = int(float(ts))
        if _intv not in intervals:
            intervals[_intv] = 1
        else:
            intervals[_intv] += 1
    interval_vals = intervals.values()
    _min = min(interval_vals)
    _max = max(interval_vals)
    _average = math.ceil(sum(interval_vals) / len(interval_vals)) if interval_vals else 0

    assert result[0][1].min == _min
    assert result[0][1].max == _max
    assert result[0][1].average == _average


@pytest.mark.asyncio
async def test_total_amout_of_bytes_exchanged(squid_log, config):
    logs = squid_log(100, 60)
    reader = StringReader(logs)
    provider = SquidProvider()
    conf = config(operations=[OperationAlias.total_amout_of_bytes_exchanged], provider=Provider.squid)
    result = await provider.process(reader, conf)

    _res = 0
    _retempl = re.compile(r'\s+')
    for line in logs.split(os.linesep):
        if not line.strip():
            continue
        cols = _retempl.split(line)
        _res += int(cols[1]) + int(cols[4])

    assert result[0][1] == _res
