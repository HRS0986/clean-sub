import re
from .config import REMOVE_EMPTY
from typing import List, Pattern
from .dtypes import ASSSubPart
from .dtypes import ASSRegexResults
from .clean import CleanSub


class CleanSubASS(CleanSub):
    def __init__(self, sub_file_path: str):
        ASS_CONTENT_PTN = r'(D.+: \d,)(\d:\d\d:\d\d\.\d{2,3},\d:\d\d:\d\d\.\d{2,3})(,\w+,.*,\d,\d,\d,.*?,)(.+)'
        super(CleanSubASS, self).__init__(sub_file_path, 'ass', ASS_CONTENT_PTN)
        self._info_content: List[str] = []
        self.__EMPTY_PTN = r'(D.+: \d,)(\d:\d\d:\d\d\.\d{2,3},\d:\d\d:\d\d\.\d{2,3})(,\w+,.*,\d,\d,\d,.*,)$'
        self.__GRAPHICS_PTN = r'\[Graphics\]\n(.+\n)*'
        self.__FONTS_PTN = r'\[Fonts\]\n(.+\n)*'
        self.__EMPTY_REGEX: Pattern[str] = re.compile(self.__EMPTY_PTN)
        self.__GRAPHICS_REGEX: Pattern[str] = re.compile(self.__GRAPHICS_PTN)
        self.__FONTS_REGEX: Pattern[str] = re.compile(self.__FONTS_PTN)

    def extract_subtitles(self, remove_empty: bool = REMOVE_EMPTY):
        with open(self._sub_file_path, 'r', encoding='utf8') as sub_file:
            sub_lines = sub_file.readlines()
            for line in sub_lines:
                if self._CONTENT_REGEX.match(line):
                    content: ASSRegexResults = self._CONTENT_REGEX.findall(line)[0]
                    sub_part: ASSSubPart = {
                        "part_1": content[0],
                        "timestamp": content[1],
                        "part_2": content[2],
                        "content": content[3]
                    }
                    self._extracted_sub_content.append(sub_part)
                else:
                    # Split script information of the ass file
                    if self.__EMPTY_REGEX.match(line):
                        if not remove_empty:
                            info_content: ASSRegexResults = self.__EMPTY_REGEX.findall(line)[0]
                            info_part: ASSSubPart = {
                                "part_1": info_content[0],
                                "timestamp": info_content[1],
                                "part_2": info_content[2],
                                "content": ''
                            }
                            self._extracted_sub_content.append(info_part)
                    else:
                        self._info_content.append(line)
            self._extracted_full_content = self._extracted_sub_content

    def create_new_sub_file(self) -> str:
        filename = self._get_file_name()
        with open(filename, 'w', encoding='utf8') as sub_file:
            for info in self._info_content:
                sub_file.write(info + '\n')

            for content in self._content_to_write:
                sub = f"{content['part_1']}{content['timestamp']}{content['part_2']}{content['content']}\n"
                sub_file.write(sub)
        return filename

    def remove_graphics_and_fonts(self):
        info_str: str = ''.join(self._info_content)

        if self.__GRAPHICS_REGEX.search(info_str):
            info_str = self.__GRAPHICS_REGEX.sub("", info_str)
        if self.__FONTS_REGEX.search(info_str):
            info_str = self.__FONTS_REGEX.sub("", info_str)

        info: List[str] = info_str.split('\n')
        for line in info[::-1]:
            if len(line) == 0:
                info.pop()
            else:
                break
        self._info_content = info