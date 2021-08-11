import os
from typing import Tuple, Union
from colorama import init, Fore
from PyInquirer import prompt

from config.config import ConfigHandler
from dtypes import ContentList
from core.ass import CleanSubASS
from core.smi import CleanSubSmi
from core.srt import CleanSubSRT

if os.name == "posix":
    init()
elif os.name == 'nt':
    init(convert=True)

Cleaner = Union[CleanSubASS, CleanSubSRT, CleanSubSmi]


def create_cleaner(filetype: str, config_handler: ConfigHandler) -> Cleaner:
    """
    :param filetype: Subtitle file's type
    :param config_handler: ConfigHandler object contains configuration settings
    :return: Cleaner object
    """
    if filetype == "srt":
        return CleanSubSRT(config_handler)
    elif filetype == 'smi':
        return CleanSubSmi(config_handler)
    else:
        return CleanSubASS(config_handler)


def detect_unwanted(cleaner: Cleaner) -> Tuple[ContentList, Cleaner]:
    """
    Detect unwanted content in the subtitle file's content
    :param cleaner: Cleaner object
    :return: Detected unwanted content and provided cleaner object
    """
    cleaner.extract_subtitles()
    if cleaner.filetype == 'ass':
        cleaner.remove_graphics_and_fonts()
    cleaner.detect_unwanted_by_content()
    cleaner.detect_unwanted_by_duration()
    return cleaner.get_unwanted(), cleaner


def select_to_remove(unwanted_content: ContentList, filetype: str) -> list:
    """
    ASk user what to remove among detected unwanted content
    :param unwanted_content: Detected unwanted content
    :param filetype: Subtitle file's type
    :return: List containing what to remove from subtitle file's content
    """
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


def clean_sub_file(unwanted_content: ContentList, cleaner: Cleaner, selected: list):
    """
    Remove unwanted content from subtitle file's content
    :param unwanted_content: Detected unwanted content fom subtitle file's content
    :param cleaner: Cleaner object
    :param selected: Content to remove among unwanted_content from subtitle file's content
    """
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


def execute(config_handler: ConfigHandler, sub_type: str):
    """
    Starting function
    :param config_handler: ConfigHandler object containing configuration settings
    :param sub_type: Subtitle file's type
    """
    sub_cleaner: Cleaner = create_cleaner(sub_type, config_handler)
    detected_content, sub_cleaner = detect_unwanted(sub_cleaner)

    is_cleaned: bool = len(detected_content) == 0

    if not is_cleaned:
        selected_content: list = select_to_remove(detected_content, sub_type)
        clean_sub_file(detected_content, sub_cleaner, selected_content)
    else:
        print(Fore.LIGHTYELLOW_EX + '\n --> Nothing To Remove In This Subtitle File\n' + Fore.RESET)
