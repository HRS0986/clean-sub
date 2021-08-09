from argparse import ArgumentParser
from cleanUI import execute
from pathlib import Path
from config.config import ConfigHandler


parser = ArgumentParser(
    description="Remove Annoying Stuff From Subtitle Files",
    prog="cleansub",
    epilog="By Hirusha Fernando",
    usage="%(prog)s [--file FILE] [--max MAX] [--min MIN] [--no-empty] [--new | --ext] [--keywords KEYWORDS | --additional KEYWORDS --exclude KEYWORDS]"
)
parser.add_argument(
    '-s',
    '--save',
    help="Save configuration to script file",
    type=str,
    dest="SCRIPT_NAME"
)

parser.add_argument(
    '-m',
    '--max',
    help="Maximum subtitle display duration to check",
    type=int,
    dest="MAX"
)
parser.add_argument(
    '-n',
    '--min',
    help="Minimum subtitle display duration to check",
    type=int,
    dest="MIN"
)
parser.add_argument(
    '-f',
    '--file',
    help="Subtitle file path",
    type=Path,
    dest="FILE"
)
parser.add_argument(
    '-e',
    '--no-empty',
    help="Remove empty content lines",
    action="store_true"
)
parser.add_argument(
    '-k',
    '--keywords',
    help="Keywords checklist",
    type=str,
    dest="KEYWORDS",
    nargs="+"
)
parser.add_argument(
    '-r',
    '--exclude',
    help="Keywords to exclude from default checklist",
    type=str,
    dest="EX_KEYWORDS",
    nargs="+"
)
parser.add_argument(
    '-a',
    '--add',
    help="Keywords to add default checklist",
    type=str,
    dest="EX_KEYWORDS",
    nargs="+"
)

group_file = parser.add_mutually_exclusive_group()
group_file.add_argument(
    '-c',
    '--new',
    help="Create new subtitle file without annoying stuff",
    action="store_true"
)
group_file.add_argument(
    '-x',
    '--ext',
    help="Modify current subtitle file without annoying stuff",
    action="store_true"
)

args = parser.parse_args()

print(args)

config_handler = ConfigHandler()
