from dataclasses import dataclass
from typing import List

from .provider.factory import Provider
from .operations import OperationAlias
from .response.formats import Format


@dataclass
class Config:
    provider: Provider
    input_files: List[str]
    output_file: str
    output_format: Format
    operation: OperationAlias

    @staticmethod
    def load_from_args(args):
        return Config(
            provider=Provider(args.provider),
            input_files=args.file,
            output_file=args.destination,
            output_format=Format(args.format),
            operation=OperationAlias(args.operation)
        )
