import json
import os
from argparse import ArgumentParser
from pathlib import Path

from PyInquirer import prompt
from mypy.api import Tuple
from prompt_toolkit.validation import Validator, ValidationError

from cleanUI import execute
from config.config import ConfigHandler

DEFAULT_CONFIGURATIONS_PATH = r'config/default_config.json'


class PathValidator(Validator):
    """
    Validator for validate user entered subtitle file's path
    """
    def validate(self, document):
        with open(DEFAULT_CONFIGURATIONS_PATH) as config_file:
            default_settings = json.load(config_file)
            FILE_TYPES = default_settings.get("FILE_TYPES")
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
    """
    Ask subtitle files location from user
    :return: subtitle file's path and filetype
    """
    question_1 = {
        "type": "input",
        "name": "sub_file_path",
        "message": "Enter Subtitle File Path: ",
        "validate": PathValidator
    }
    answer_1: dict = prompt(question_1)
    sub_file_path: str = answer_1['sub_file_path'].strip('"')
    sub_file_path = sub_file_path.strip("' ")
    file_type: str = sub_file_path[-3:]
    return sub_file_path, file_type


if __name__ == '__main__':
    parser = ArgumentParser(
        description="Remove Annoying Stuff From Subtitle Files",
        prog="cleansub",
        epilog="By Hirusha Fernando",
        usage="%(prog)s [-h] [-f FILE] [-m MAX] [-n MIN] [-e | -g] [-c | -x] [-k KEYWORDS | -a KEYWORDS -r KEYWORDS] [-s SCRIPT_SAVE NAME | -u SCRIPT_NAME]"
    )
    parser.add_argument('-m', '--max', help="Maximum subtitle display duration to check", type=int, dest="MAX")
    parser.add_argument('-n', '--min', help="Minimum subtitle display duration to check", type=int, dest="MIN")
    parser.add_argument('-f', '--file', help="Subtitle file path", type=Path, dest="FILE")
    parser.add_argument('-k', '--keywords', help="Keywords checklist (Comma Separated)", type=str, dest="K", nargs="+")
    parser.add_argument('-r', '--exc', help="Keywords to exclude from default list (Comma Separated)", type=str, dest="EX_K", nargs="+")
    parser.add_argument('-a', '--add', help="Keywords to add default list (Comma Separated)", type=str, dest="ADD_K", nargs="+")

    group_script = parser.add_mutually_exclusive_group()
    group_script.add_argument('-s', '--save', help="Save configuration to script file", type=str, dest="SCRIPT_SAVE_NAME")
    group_script.add_argument('-u', '--use', help="Use another configuration script file", type=str, dest="SCRIPT_NAME")

    group_empty = parser.add_mutually_exclusive_group()
    group_empty.add_argument('-g', '--keep-empty', help="Keep empty content lines", action="store_true")
    group_empty.add_argument('-e', '--no-empty', help="Remove empty content lines", action="store_true")

    group_file = parser.add_mutually_exclusive_group()
    group_file.add_argument('-c', '--new', help="Create new subtitle file", action="store_true")
    group_file.add_argument('-x', '--ext', help="Modify current subtitle file", action="store_true")

    args = parser.parse_args()

    if args.K and args.EX_K:
        parser.error('argument -k/--keywords: not allowed with argument -r/--exc')

    if args.K and args.ADD_K:
        parser.error('argument -k/--keywords: not allowed with argument -a/--add')

    # NOTE: Set filetype and sub file path
    sub_path, filetype = '', ''
    if not args.FILE:
        sub_path, filetype = take_sub_file_from_user()
    else:
        sub_path = args.FILE
        filetype = sub_path[-3:]

    config_handler = ConfigHandler(
        sub_path,
        filetype,
        args.no_empty,
        args.keep_empty,
        args.MIN,
        args.MAX,
        args.SCRIPT_SAVE_NAME,
        args.SCRIPT_NAME,
        args.new,
        args.ext,
        args.K,
        args.ADD_K,
        args.EX_K
    )

    execute(config_handler, filetype)
