"""
A one cli for all the anime.
"""

import click

from .core import package_banner
from .core.cli.commands import download, stream, continuation, grab, schedule, test
from .core.cli.helpers.player import supported_streamers

print("\x1b[35m{}\x1b[39m".format(package_banner))

commands = {
    'download': download.animdl_download,
    'continue': continuation.animdl_continue,
    'grab': grab.animdl_grab,
    'schedule': schedule.animdl_schedule,
    'test': test.animdl_test
}

executable = [*supported_streamers()]

if executable:
    commands.update({'stream': stream.animdl_stream})
	
@click.group(commands=commands)
def __animdl_cli__():
    pass