import re

from config.config import ConfigHandler
from abc import abstractmethod, ABC
from typing import List, Union, Pattern
from dtypes import ContentList, SplitTimestamp


class CleanSub(ABC):
    def __init__(self, sub_file_path: str, filetype: str, content_pattern: str, config_handler: ConfigHandler):
        self._sub_file_path = sub_file_path
        self._extracted_sub_content: ContentList = []
        self._extracted_full_content: ContentList = []
        self._unwanted_content: ContentList = []
        self._content_to_write: ContentList = []
        self._config_handler = config_handler
        self.filetype = filetype
        self.__CONTENT_PATTERN = content_pattern
        self._CONTENT_REGEX: Pattern[str] = re.compile(self.__CONTENT_PATTERN)

    def _calculate_duration(self, start: List[int], end: List[int]) -> float:
        """
        Calculate subtitle's display duration
        """
        duration = 0.000
        s_seconds, s_minutes, s_hours = start[-1], start[1], start[0]
        e_seconds, e_minutes, e_hours = end[-1], end[1], end[0]

        if e_seconds < s_seconds:
            e_seconds += 60
            e_minutes -= 1
        if e_minutes < s_minutes:
            e_minutes += 60
            e_hours -= 1

        duration += e_seconds - s_seconds
        duration += (e_minutes - s_minutes) * 60
        duration += (e_hours - s_hours) * 60 * 60

        duration = float(f'{duration:.3f}')
        return duration

    def _split_timestamp(self, timestamp: str) -> SplitTimestamp:
        start, end, sec_separator = '', '', ','
        if self.filetype == 'srt':
            start, end = timestamp.split(' --> ')

        elif self.filetype == 'ass':
            start, end = timestamp.split(',')
            sec_separator = '.'

        elif self.filetype == 'smi':
            start, end = timestamp.split('-')
            smi_sms, smi_ems = int(start[-3:]), int(end[-3:])
            smi_start, smi_end = int(start[:-3]), int(end[:-3])
            smi_sh, smi_eh = smi_start // 3600, smi_end // 3600
            smi_start, smi_end = smi_start % 3600, smi_end % 3600
            smi_sm, smi_em = smi_start // 60, smi_end // 60
            smi_ss, smi_es = smi_start % 60, smi_end % 60
            s_sec = float(f"{smi_ss}.{smi_sms}")
            e_sec = float(f"{smi_es}.{smi_ems}")
            return {'start': [smi_sh, smi_sm, s_sec], 'end': [smi_eh, smi_em, e_sec]}

        sh, sm, ss = start.split(':')
        ss, sms = ss.split(sec_separator)
        eh, em, es = end.split(':')
        es, ems = es.split(sec_separator)
        s_sec = float('.'.join((ss, sms)))
        e_sec = float('.'.join((es, ems)))

        return {'start': [int(sh), int(sm), s_sec], 'end': [int(eh), int(em), e_sec]}

    def get_unwanted(self) -> ContentList:
        return self._unwanted_content

    def detect_unwanted_by_content(self):
        after_content: ContentList = []
        for content in self._extracted_sub_content:
            sub_content = ' '.join(content['content']) if self.filetype == 'srt' else content['content']
            for keyword in self._config_handler.keywords:
                if keyword in sub_content:
                    self._unwanted_content.append(content)
                    break
            else:
                after_content.append(content)
        self._extracted_sub_content = after_content

    def detect_unwanted_by_duration(self):
        after_duration: ContentList = []
        for content in self._extracted_sub_content:
            split_timestamp: SplitTimestamp = self._split_timestamp(content['timestamp'])
            start: List[Union[int, float]] = split_timestamp['start']
            end: List[Union[int, float]] = split_timestamp['end']
            duration = self._calculate_duration(start, end)
            if duration <= self._config_handler.min:
                self._unwanted_content.append(content)
            elif duration >= self._config_handler.max:
                self._unwanted_content.append(content)
            else:
                after_duration.append(content)
        self._extracted_sub_content = after_duration

    def remove_unwanted(self, content_to_remove: ContentList):
        for content in self._extracted_full_content:
            if content in content_to_remove:
                content_to_remove.remove(content)
                continue
            self._content_to_write.append(content)

    def _get_file_name(self) -> str:
        """
        Return new subtitle file's name
        """
        if self._config_handler.new_file:
            return f'{self._sub_file_path[:-4]}-NEW.{self.filetype}'
        else:
            return self._sub_file_path

    @abstractmethod
    def extract_subtitles(self):
        pass

    @abstractmethod
    def create_new_sub_file(self) -> str:
        pass
