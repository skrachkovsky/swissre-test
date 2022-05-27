from io import StringIO
import os
import typing
from abc import ABC


class DataReader(ABC):
    async def read(self) -> typing.AsyncGenerator[str, None]:
        ...


class FileReader(DataReader):
    def __init__(self, *filepath: str):
        self._inputs = []
        for fp in filepath:
            if os.path.isdir(fp):
                self._inputs += self._process_dir(fp)
            else:
                self._inputs.append(self._open_file(fp))

    def _process_dir(self, filepath: str):
        return [self._open_file(f) for f in os.listdir(filepath) if os.path.isfile(f)]

    def _open_file(self, filename: str):
        return open(filename, 'r')

    async def read(self) -> typing.AsyncGenerator[str, None]:
        for inp in self._inputs:
            with inp as file:
                for line in file:
                    line = await self.process_line(line)
                    if line is None:
                        continue
                    yield line

    async def process_line(self, line: str) -> typing.Union[str, None]:
        if not line.strip():
            return
        return line


class StringReader(DataReader):
    def __init__(self, *logs_strings):
        self._logs_strings = logs_strings

    async def read(self) -> typing.AsyncGenerator[str, None]:
        for log in self._logs_strings:
            with StringIO(log) as log_res:
                for line in log_res:
                    line = await self.process_line(line)
                    if line is None:
                        continue
                    yield line

    async def process_line(self, line: str) -> typing.Union[str, None]:
        line = line.strip('\n').strip('\r')
        if not line.strip():
            return
        return line
