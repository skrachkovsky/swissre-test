import argparse
import asyncio
from time import time

from .config import Config
from .readers import FileReader
from .operations import OperationAlias
from .response import FileResponse, FormatAlias
from .squid import SquidProvider
from .logger import logger


async def main():
    parser = argparse.ArgumentParser(
        description='A command line tool to analyze the content of log files. '
        'The tool should accept arguments as input and return '
        'an output after having performed operations on the given input.')

    parser.add_argument('file', nargs='+', help='Path to one or more plain text files, or a directory')
    parser.add_argument('operation', choices=[al.value for al in OperationAlias], help=OperationAlias.__doc__)
    parser.add_argument('destination', help='Path to a file to save output in plain text')
    parser.add_argument('format', choices=[al.value for al in FormatAlias], help='Output data format')

    args = parser.parse_args()
    config = Config.load_from_args(args)
    start_time = time()
    err = None
    result = None

    try:
        reader = FileReader(*config.input_files)
        provider = SquidProvider()
        result = await provider.process(config.operation, reader, config)
    except Exception as exc:
        logger.exception(exc)
        err = exc
    finally:
        response = FileResponse(
            filename=config.output_file,
            result=result,
            operation=config.operation,
            error=err,
            output_format=FormatAlias(config.output_format).get_object()
        )
        res = await response.save()
        print(f'Result: {res.result}')
    print(f'Executoin time: {time() - start_time}')


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
