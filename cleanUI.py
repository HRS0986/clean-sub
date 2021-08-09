import os
from typing import Tuple, Union
from colorama import init, Fore
from PyInquirer import prompt, Validator, ValidationError
from dtypes import ContentList
from core.ass import CleanSubASS
from core.smi import CleanSubSmi
from core.srt import CleanSubSRT
from config.default_config import FILE_TYPES

if os.name == "posix":
    init()
elif os.name == 'nt':
    init(convert=True)

Cleaner = Union[CleanSubASS, CleanSubSRT, CleanSubSmi]


class PathValidator(Validator):
    def validate(self, document):
        valid_path: bool = os.path.isfile(document.text)
        valid_type: bool = document.text[-3:] in FILE_TYPES
        if not valid_path and valid_type:
            raise ValidationError(
                message="Invalid file. Please enter valid file path",
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


def create_cleaner(sub_file_path: str, filetype: str) -> Cleaner:
    if filetype == "srt":
        return CleanSubSRT(sub_file_path)
    elif filetype == 'smi':
        return CleanSubSmi(sub_file_path)
    else:
        return CleanSubASS(sub_file_path)


def detect_unwanted(cleaner: Cleaner) -> Tuple[ContentList, Cleaner]:
    cleaner.extract_subtitles()
    if cleaner.filetype == 'ass':
        cleaner.remove_graphics_and_fonts()
    cleaner.detect_unwanted_by_content()
    cleaner.detect_unwanted_by_duration()
    return cleaner.get_unwanted(), cleaner


def select_to_remove(unwanted_content: ContentList, filetype: str) -> list:
    question_2 = {
        "type": "checkbox",
        "name": "unwanted",
        "message": "Select what to remove:",
        "choices": [
            {
                "name": f"{sub['timestamp']} :- {','.join(sub['content']) if filetype == 'srt' else sub['content']}",
                "checked": True
            } for sub in unwanted_content
        ],
    }
    answers_2: list = prompt(question_2)['unwanted']
    return answers_2


def clean_sub_file(unwanted_content: ContentList, cleaner: Cleaner, selected: list) -> None:
    to_remove: ContentList = []
    for sub in selected:
        timestamp = sub.split(' :- ')[0]
        for content in unwanted_content:
            if content['timestamp'] == timestamp:
                to_remove.append(content)
                unwanted_content.remove(content)
                break

    cleaner.remove_unwanted(to_remove)
    filename: str = cleaner.create_new_sub_file()
    print(Fore.BLUE + f"\n --> File Saved To {filename}\n" + Fore.RESET)


def execute():
    subtitle_path, sub_type = take_sub_file_from_user()
    sub_cleaner: Cleaner = create_cleaner(subtitle_path, sub_type)
    detected_content, sub_cleaner = detect_unwanted(sub_cleaner)

    is_cleaned: bool = len(detected_content) == 0

    if not is_cleaned:
        selected_content: list = select_to_remove(detected_content, sub_type)
        clean_sub_file(detected_content, sub_cleaner, selected_content)
    else:
        print(Fore.LIGHTYELLOW_EX + '\n --> Nothing To Remove In This Subtitle File\n' + Fore.RESET)
