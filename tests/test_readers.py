import pytest
import os
from swissre_test.readers import StringReader


@pytest.mark.asyncio
async def test_string_reader():
    reader = StringReader(os.linesep.join(map(str, range(10))))
    i = 0
    async for line in reader.read():
        assert line == str(i)
        i += 1
