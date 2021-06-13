from PyInquirer import prompt, Validator, ValidationError
import os
# from pprint import pprint
from clean import CleanSub
# from colorama import init, Fore

# init(convert=True)


class PathValidator(Validator):
    def validate(self, document):
        valid_path = os.path.isfile(document.text)
        if not valid_path:
            raise ValidationError(
                message="Invalid path. Please enter valid path",
                cursor_position=len(document.text)
            )


question_1 = {
    "type": "input",
    "name": "sub_file_path",
    "message": "Enter Subtitle File Path: ",
    "validate": PathValidator
}

answer = prompt(question_1)
sub_file_path = answer['sub_file_path']

cleaner = CleanSub(sub_file_path)
cleaner.extract_subtitles()
cleaner.detect_unwanted_by_content()
cleaner.detect_unwanted_by_duration()
unwanted_content = cleaner.get_unwanted()

question_2 = {
    "type": "checkbox",
    "name": "unwanted",
    "message": "Select what to remove:",
    "choices": [
        {
            "name": f"{content['timestamp']} :- {','.join(content['content'])}",
            "checked": True
        } for content in unwanted_content
    ],
}

answers = prompt(question_2)['unwanted']

to_remove: list[dict] = []
for answer in answers:
    timestamp = answer.split(' :- ')[0]
    for content in unwanted_content:
        if content['timestamp'] == timestamp:
            to_remove.append(content)
            break

cleaner.remove_unwanted(to_remove)
filename: str = cleaner.create_new_sub_file()
print(f"File Saved To {filename}")

