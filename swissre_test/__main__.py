import argparse
import asyncio
from time import time

from .config import Config
from .readers import FileReader, StdinReader
from .operations import OperationAlias
from .response import FileResponse, StdoutResponse
from .response.formats import Format
from .provider.factory import Provider
from .logger import logger


async def main():
    parser = argparse.ArgumentParser(
        description='A command line tool to analyze the content of log files. '
        'The tool should accept arguments as input and return '
        'an output after having performed operations on the given input.')

    parser.add_argument('provider', choices=[pr.value for pr in Provider], help='Different input log formats')
    parser.add_argument('--file', nargs='+', help='Path to one or more plain text files, or a directory')
    parser.add_argument('operation', nargs='+',
                        choices=[al.value for al in OperationAlias], help=OperationAlias.__doc__)
    parser.add_argument('--destination', help='Path to a file to save output in plain text')
    parser.add_argument('format', choices=[fmt.value for fmt in Format], help='Output data format')

    args = parser.parse_args()
    config = Config.load_from_args(args)
    start_time = time()

    if config.input_files == ['stdin']:
        reader = StdinReader()
    else:
        reader = FileReader(*config.input_files)
    provider = config.provider.get_object()
    results = await provider.process(reader, config)
    output_format = Format(config.output_format).get_object()
    if config.output_file == 'stdout':
        response = StdoutResponse(output_format, results)
    else:
        response = FileResponse(config.output_file, output_format, results)
    await response.save()

    logger.debug(f'Executoin time: {time() - start_time}')


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
