from dataclasses import dataclass
from typing import List

from .operations import OperationAlias
from .response import FormatAlias


@dataclass
class Config:
    input_files: List[str]
    output_file: str
    output_format: FormatAlias
    operation: OperationAlias

    @staticmethod
    def load_from_args(args):
        return Config(
            input_files=args.file,
            output_file=args.destination,
            output_format=FormatAlias(args.format),
            operation=OperationAlias(args.operation)
        )
