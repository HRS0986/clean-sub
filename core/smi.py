import re
from typing import Dict

from config.config import ConfigHandler
from dtypes import SMISubPart, SMIRegexResults
from .clean import CleanSub


class CleanSubSmi(CleanSub):
    def __init__(self, config_handler: ConfigHandler):
        SMI_CONTENT_PATTERN = r"(<SYNC.+)\n(.+)\n(<SYNC .+?nbsp)"
        super(CleanSubSmi, self).__init__(SMI_CONTENT_PATTERN, config_handler)
        self._info_content: Dict[str, str] = {"head": "", "tale": "\n</BODY>\n</SAMI>"}
        self.__INFO_HEAD_PATTERN = r"<SAMI>.+<BODY>\n"
        self.__TIMESTAMP_PATTERN = r"Start=(\d+?)>"
        self.__INFO_HEAD_REGEX = re.compile(self.__INFO_HEAD_PATTERN, flags=re.DOTALL)
        self.__TIMESTAMP_REGEX = re.compile(self.__TIMESTAMP_PATTERN)

    def extract_subtitles(self):
        """
        Read and split subtitle file's content
        """
        with open(self._sub_file_path, 'r', encoding='utf16', errors='ignore') as sub_file:
            sub_content: str = sub_file.read()
            content_results: SMIRegexResults = self._CONTENT_REGEX.findall(sub_content)
            for result_group in content_results:
                start = self.__TIMESTAMP_REGEX.findall(result_group[0])[0]
                end = self.__TIMESTAMP_REGEX.findall(result_group[2])[0]
                sub_part: SMISubPart = {
                    "start": result_group[0],
                    "end": result_group[2],
                    "timestamp": f"{start}-{end}",
                    "content": result_group[1]
                }
                self._extracted_sub_content.append(sub_part)
            self._extracted_full_content = self._extracted_sub_content

            info_results: str = self.__INFO_HEAD_REGEX.findall(sub_content)[0]
            self._info_content['head'] = info_results

    def create_new_sub_file(self) -> str:
        filename = self._get_file_name()
        with open(filename, 'w', encoding='utf16') as sub_file:
            sub_file.write(self._info_content['head'])
            for content in self._content_to_write:
                sub = f"{content['start']}\n{content['content']}\n{content['end']}\n"
                sub_file.write(sub)
            sub_file.write(self._info_content['tale'])
        return filename
