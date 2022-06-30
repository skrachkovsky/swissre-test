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
    operations: List[OperationAlias]

    @staticmethod
    def load_from_args(args):
        return Config(
            provider=Provider(args.provider),
            input_files=args.file,
            output_file=args.destination,
            output_format=Format(args.format),
            operations=[OperationAlias(op) for op in args.operation]
        )
