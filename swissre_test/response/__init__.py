import os
import typing
from datetime import datetime
from abc import ABC, abstractmethod

from ..entities import ResponseError, ResponseEntity

if typing.TYPE_CHECKING:
    from ..operations import OperationAlias
    from .formats import ResponseFormat


class Response(ABC):
    def __init__(self, operation: 'OperationAlias', output_format: 'ResponseFormat', result: typing.Any = None,
                 error: typing.Optional[Exception] = None):
        self._operation = operation
        self._result = result
        self._error = error
        self._output_format = output_format

    @abstractmethod
    async def save(self):
        raise NotImplementedError

    async def build_response(self) -> ResponseEntity:
        return ResponseEntity(
            timestamp=datetime.now().timestamp(),
            operation=self._operation.name,
            result=self._result,
            error=ResponseError(
                label=self._error.__class__.__name__,
                details=str(self._error)
            ) if self._error else None
        )


class FileResponse(Response):
    def __init__(self, filename: str, operation: 'OperationAlias', output_format: 'ResponseFormat',
                 result: typing.Any = None, error: typing.Optional[Exception] = None):
        self._path = os.path.abspath(filename)
        if self._path.startswith(os.path.dirname(__file__)):
            raise PermissionError('Access to the application directory is denied')
        super().__init__(operation, output_format, result, error)

    async def save(self) -> ResponseEntity:
        res = await self.build_response()
        with open(self._path, 'w') as file:
            file.write(await self._output_format.render(res))
        return res
