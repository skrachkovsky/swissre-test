import os
import typing
from datetime import datetime
from abc import ABC, abstractmethod

from ..entities import ResponseError, ResponseEntity

if typing.TYPE_CHECKING:
    from .formats import ResponseFormat


class Response(ABC):
    def __init__(self, output_format: 'ResponseFormat', results: typing.List[typing.Any]):
        self._results = results
        self._output_format = output_format

    @abstractmethod
    async def save(self):
        raise NotImplementedError

    async def build_response(self) -> typing.List[ResponseEntity]:
        return [
            ResponseEntity(
                timestamp=datetime.now().timestamp(),
                operation=operation,
                result=result if not isinstance(result, Exception) else None,
                error=ResponseError(
                    label=result.__class__.__name__,
                    details=str(result)
                ) if isinstance(result, Exception) else None
            ) for operation, result in self._results
        ]


class FileResponse(Response):
    def __init__(self, filename: str, output_format: 'ResponseFormat',
                 results: typing.List[typing.Any]):
        self._path = os.path.abspath(filename)
        if self._path.startswith(os.path.dirname(__file__)):
            raise PermissionError('Access to the application directory is denied')
        super().__init__(output_format, results)

    async def save(self) -> typing.List[ResponseEntity]:
        res = await self.build_response()
        with open(self._path, 'w') as file:
            file.write(await self._output_format.render(res))
        return res


class StdoutResponse(Response):
    async def save(self) -> typing.List[ResponseEntity]:
        res = await self.build_response()
        print(await self._output_format.render(res), flush=True, end='')
        return res
