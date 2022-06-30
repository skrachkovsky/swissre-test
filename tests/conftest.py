import pytest
import os
from datetime import datetime, timedelta
from random import randint, uniform

from swissre_test.config import Config
from swissre_test.operations import OperationAlias
from swissre_test.response.formats import Format
from swissre_test.provider.factory import Provider


@pytest.fixture
async def squid_log():
    """
    1157689324.156 1372 10.105.21.199 TCP_MISS/200 399 GET http://www[.]google-analytics[.]com/__utm.gif? badeyek DIRECT/66.102.9.147 image/gif
    """  # noqa
    def generate_log(len: int, timedelta_sec: int):
        now = datetime.now()
        stop_time: float = now.timestamp()
        start_time: float = (now - timedelta(seconds=timedelta_sec)).timestamp()
        res = []
        files = {}
        for _ in range(len):
            file = f'http://www[.]google-analytics[.]com/__utm{randint(1, 20)}.gif?'
            if file not in files:
                files[file] = randint(200, 2000), randint(10, 3000)
            res.append(' '.join(map(str, [
                round(uniform(start_time, stop_time), 3),
                files[file][0],
                f'192.168.1.{randint(2, 255)}',
                'TCP_MISS/200',
                files[file][1],
                'GET',
                file,
                f'badeyek{randint(1, 10)}',
                f'DIRECT/192.168.2.{randint(2, 255)}',
                'image/gif'
            ])))
        return os.linesep.join([''] + sorted(res))
    yield generate_log


@pytest.fixture
async def config():
    def conf(**kwargs):
        return Config(
            input_files=kwargs.get('input_files', ['access.log']),
            output_file=kwargs.get('output_file', 'output.txt'),
            output_format=Format(kwargs.get('output_format', Format.json)),
            operations=[OperationAlias(op) for op in kwargs['operations']],
            provider=Provider(kwargs['provider'])
        )
    yield conf
