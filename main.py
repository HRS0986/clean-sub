import os
from argparse import ArgumentParser

from PyInquirer import prompt
from mypy.api import Tuple
from prompt_toolkit.validation import Validator, ValidationError

from cleanUI import execute
from pathlib import Path
from config.config import ConfigHandler
from config.default_config import FILE_TYPES


class PathValidator(Validator):
    def validate(self, document):
        valid_path: bool = os.path.isfile(document.text)
        valid_type: bool = document.text[-3:] in FILE_TYPES
        if not valid_path:
            raise ValidationError(
                message="Invalid file path. Please enter valid file path",
                cursor_position=len(document.text)
            )
        elif not valid_type:
            raise ValidationError(
                message="Unsupported file. Please enter valid file path",
                cursor_position=len(document.text)
            )


def take_sub_file_from_user() -> Tuple[str, str]:
    question_1 = {
        "type": "input",
        "name": "sub_file_path",
        "message": "Enter Subtitle File Path: ",
        "validate": PathValidator
    }

    answer_1: dict = prompt(question_1)
    sub_file_path: str = answer_1['sub_file_path'].strip('"')
    sub_file_path = sub_file_path.strip("' ")
    filetype: str = sub_file_path[-3:]
    return sub_file_path, filetype


parser = ArgumentParser(
    description="Remove Annoying Stuff From Subtitle Files",
    prog="cleansub",
    epilog="By Hirusha Fernando",
    usage="%(prog)s [--file FILE] [--max MAX] [--min MIN] [--no-empty] [--new | --ext] [--keywords KEYWORDS | --additional KEYWORDS --exclude KEYWORDS]"
)
parser.add_argument('-s', '--save', help="Save configuration to script file", type=str, dest="SCRIPT_NAME")
parser.add_argument('-m', '--max', help="Maximum subtitle display duration to check", type=int, dest="MAX")
parser.add_argument('-n', '--min', help="Minimum subtitle display duration to check", type=int, dest="MIN")
parser.add_argument('-f', '--file', help="Subtitle file path", type=Path, dest="FILE")
parser.add_argument('-e', '--no-empty', help="Remove empty content lines", action="store_true")
parser.add_argument('-k', '--keywords', help="Keywords checklist (Comma Separated)", type=str, dest="K", nargs="+")
parser.add_argument('-r', '--exc', help="Keywords to exclude from default list (Comma Separated)", type=str, dest="EX_K", nargs="+")
parser.add_argument('-a', '--add', help="Keywords to add default list (Comma Separated)", type=str, dest="ADD_K", nargs="+")

group_file = parser.add_mutually_exclusive_group()
group_file.add_argument('-c', '--new', help="Create new subtitle file", action="store_true")
group_file.add_argument('-x', '--ext', help="Modify current subtitle file", action="store_true")

args = parser.parse_args()

print(args.K)
#
# subtitle_path, sub_type = take_sub_file_from_user()
# config_handler = ConfigHandler(min_d=args.MIN, max_d=args.MAX, empty=args.e, new_file=args.NEW)

# TODO: Pass all args to ConfigHandler and process args in the class
