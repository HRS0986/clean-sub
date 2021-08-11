from typing import List

from config.config import ConfigHandler
from dtypes import SRTRegexResults, SRTSubPart
from .clean import CleanSub


class CleanSubSRT(CleanSub):
    def __init__(self, config_handler: ConfigHandler):
        SRT_CONTENT_PATTERN = r'([0-9]+\n.+(\n.+){1,})'
        super(CleanSubSRT, self).__init__(SRT_CONTENT_PATTERN, config_handler)

    def extract_subtitles(self) -> None:
        """
        Read and split subtitle file's content
        """
        with open(self._sub_file_path, 'r', encoding='utf8') as sub_file:
            sub_content: str = sub_file.read()
            results: SRTRegexResults = self._CONTENT_REGEX.findall(sub_content)
            for result_group in results:
                lines: List[str] = result_group[0].split('\n')
                number: str = lines[0]
                timestamp: str = lines[1]
                sub: List[str] = lines[2:]
                sub_part: SRTSubPart = {
                    'number': number,
                    'timestamp': timestamp,
                    'content': sub
                }
                self._extracted_sub_content.append(sub_part)
            self._extracted_full_content = self._extracted_sub_content

    def create_new_sub_file(self) -> str:
        filename = self._get_file_name()
        with open(filename, 'w', encoding='utf8') as sub_file:
            for i, content in enumerate(self._content_to_write, 1):
                sub_content = '\n'.join(content['content'])
                sub = f"{i}\n{content['timestamp']}\n{sub_content}\n\n"
                sub_file.write(sub)
        return filename
