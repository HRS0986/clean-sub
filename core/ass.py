import re

from config.config import ConfigHandler
from typing import List, Pattern
from dtypes import ASSSubPart
from dtypes import ASSRegexResults
from .clean import CleanSub


class CleanSubASS(CleanSub):
    def __init__(self, config_handler: ConfigHandler):
        ASS_CONTENT_PATTERN = r'(D.+: \d,)(\d:\d\d:\d\d\.\d{2,3},\d:\d\d:\d\d\.\d{2,3})(,\w+,.*,\d,\d,\d,.*?,)(.+)'
        super(CleanSubASS, self).__init__(ASS_CONTENT_PATTERN, config_handler)
        self._info_content: List[str] = []
        self.__EMPTY_PATTERN = r'(D.+: \d,)(\d:\d\d:\d\d\.\d{2,3},\d:\d\d:\d\d\.\d{2,3})(,\w+,.*,\d,\d,\d,.*,)$'
        self.__GRAPHICS_PATTERN = r'\[Graphics\]\n(.+\n)*'
        self.__FONTS_PATTERN = r'\[Fonts\]\n(.+\n)*'
        self.__EMPTY_REGEX: Pattern[str] = re.compile(self.__EMPTY_PATTERN)
        self.__GRAPHICS_REGEX: Pattern[str] = re.compile(self.__GRAPHICS_PATTERN)
        self.__FONTS_REGEX: Pattern[str] = re.compile(self.__FONTS_PATTERN)

    def extract_subtitles(self):
        """
        Read and split subtitle file's content into
            - subtitle content
            - script information
            - empty subtitle lines
        """
        with open(self._sub_file_path, 'r', encoding='utf8') as sub_file:
            sub_lines = sub_file.readlines()
            for line in sub_lines:
                # Extract subtitle content line
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
                    # Extract empty content Lines
                    if self.__EMPTY_REGEX.match(line):
                        if not self._config_handler.remove_empty:
                            info_content: ASSRegexResults = self.__EMPTY_REGEX.findall(line)[0]
                            info_part: ASSSubPart = {
                                "part_1": info_content[0],
                                "timestamp": info_content[1],
                                "part_2": info_content[2],
                                "content": ''
                            }
                            self._extracted_sub_content.append(info_part)
                    else:
                        # Collect script information of the ass file
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
        """
        Remove [GRAPHICS] section and [FONT] section in ass file
        """
        info_str: str = ''.join(self._info_content)

        # Replace graphics content and font content with "" 
        if self.__GRAPHICS_REGEX.search(info_str):
            info_str = self.__GRAPHICS_REGEX.sub("", info_str)
        if self.__FONTS_REGEX.search(info_str):
            info_str = self.__FONTS_REGEX.sub("", info_str)

        # Remove graphics content and font content in ASS file's information content part
        info: List[str] = info_str.split('\n')
        for line in info[::-1]:
            if len(line) == 0:
                info.pop()
            else:
                break
        self._info_content = info
