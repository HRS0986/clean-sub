from argparse import ArgumentParser
from cleanUI import execute
from pathlib import Path


parser = ArgumentParser(
    description="Remove Annoying Stuff From Subtitle Files",
    prog="cleansub",
    epilog="By Hirusha Fernando",
    usage="%(prog)s [--file FILE] [--max MAX] [--min MIN] [--no-empty] [--new | --ext]"
)
parser.add_argument('-m', '--max', help="Maximum subtitle display duration to check", type=int, dest="MAX")
parser.add_argument('-n', '--min', help="Minimum subtitle display duration to check", type=int, dest="MIN")
parser.add_argument('-f', '--file', help="Subtitle file path", type=Path, dest="FILE")
parser.add_argument('-e', '--no-empty', help="Remove empty content lines", action="store_true")
group = parser.add_mutually_exclusive_group()
group.add_argument('-c', '--new', help="Create new subtitle file without annoying stuff", action="store_true")
group.add_argument('-x', '--ext', help="Modify current subtitle file without annoying stuff", action="store_true")

args = parser.parse_args()

print(args)