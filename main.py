from PyInquirer import prompt, Validator, ValidationError
import os
from dtypes import ContentList
# from pprint import pprint
from clean import CleanSubSRT, CleanSubASS
from typing import Union
from colorama import init, Fore

if os.name == "posix":
    init()
elif os.name == 'nt':
    init(convert=True)


class PathValidator(Validator):
    def validate(self, document):
        valid_path = os.path.isfile(document.text)
        valid_type = document.text[-3:] in ('srt', 'ass')
        if not valid_path and valid_type:
            raise ValidationError(
                message="Invalid file. Please enter valid file path",
                cursor_position=len(document.text)
            )


question_1 = {
    "type": "input",
    "name": "sub_file_path",
    "message": "Enter Subtitle File Path: ",
    "validate": PathValidator
}

answer = prompt(question_1)
sub_file_path: str = answer['sub_file_path'].strip('"')
sub_file_path: str = answer['sub_file_path'].strip("'")
filetype = sub_file_path[-3:]

cleaner: Union[CleanSubASS, CleanSubSRT]
if filetype == "srt":
    cleaner = CleanSubSRT(sub_file_path)
else:
    cleaner = CleanSubASS(sub_file_path)

cleaner.extract_subtitles()
cleaner.detect_unwanted_by_content()
cleaner.detect_unwanted_by_duration()
unwanted_content = cleaner.get_unwanted()

if (len(unwanted_content)) != 0:
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
    answers = prompt(question_2)['unwanted']

    to_remove: ContentList = []
    for answer in answers:
        timestamp = answer.split(' :- ')[0]
        for content in unwanted_content:
            if content['timestamp'] == timestamp:
                to_remove.append(content)
                break

    cleaner.remove_unwanted(to_remove)
    filename: str = cleaner.create_new_sub_file()
    print(Fore.BLUE + f"\n --> File Saved To {filename}\n" + Fore.RESET)

else:
    print(Fore.LIGHTYELLOW_EX + 'Nothing To Remove In This Subtitle File' + Fore.RESET)

