import re
from config import MIN_DURATION, MAX_DURATION, KEYWORDS, CREATE_NEW_FILE, REMOVE_EMPTY
from abc import abstractmethod, ABC
from typing import List, Union, Pattern
from dtypes import ContentList, SplitTimestamp, SRTSubPart, ASSSubPart, SRTRegexResults, ASSRegexResults


class CleanSub(ABC):
    def __init__(self, sub_file_path: str, filetype: str):
        self._sub_file_path = sub_file_path
        self._extracted_sub_content: ContentList = []
        self._extracted_full_content: ContentList = []
        self._unwanted_content: ContentList = []
        self._content_to_write: ContentList = []
        self.filetype = filetype

    def _calculate_duration(self, start: List[int], end: List[int]) -> float:
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
            for keyword in KEYWORDS:
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
            if duration <= MIN_DURATION:
                self._unwanted_content.append(content)
            elif duration >= MAX_DURATION:
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

    @abstractmethod
    def extract_subtitles(self):
        pass

    @abstractmethod
    def create_new_sub_file(self) -> str:
        pass


class CleanSubSRT(CleanSub):
    def __init__(self, sub_file_path: str):
        super(CleanSubSRT, self).__init__(sub_file_path, 'srt')

    def extract_subtitles(self) -> None:
        with open(self._sub_file_path, 'r', encoding='utf8') as sub_file:
            sub_content: str = sub_file.read()
            SUB_PATTERN = r'([0-9]+\n.+(\n.+){1,})'
            REGEX: Pattern[str] = re.compile(SUB_PATTERN)
            results: SRTRegexResults = REGEX.findall(sub_content)
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
        if CREATE_NEW_FILE:
            filename = f'{self._sub_file_path[:-4]}-NEW.{self._sub_file_path[-3:]}'
        else:
            filename = self._sub_file_path

        with open(filename, 'w', encoding='utf8') as sub_file:
            for i, content in enumerate(self._content_to_write, 1):
                sub_content = '\n'.join(content['content'])
                sub = f"{i}\n{content['timestamp']}\n{sub_content}\n\n"
                sub_file.write(sub)
        return filename


class CleanSubASS(CleanSub):
    def __init__(self, sub_file_path: str):
        super(CleanSubASS, self).__init__(sub_file_path, 'ass')
        self.info_content: List[str] = []

    def extract_subtitles(self, remove_empty: bool=REMOVE_EMPTY):
        with open(self._sub_file_path, 'r', encoding='utf8') as sub_file:
            sub_lines = sub_file.readlines()
            SUB_PATTERN = r'(D.+: \d,)(\d:\d\d:\d\d\.\d{2,3},\d:\d\d:\d\d\.\d{2,3})(,\w+,.*,\d,\d,\d,.*,)(.+)'
            REGEX: Pattern[str] = re.compile(SUB_PATTERN)
            for line in sub_lines:
                if REGEX.match(line):
                    content: ASSRegexResults = REGEX.findall(line)[0]
                    sub_part: ASSSubPart = {
                        "part_1": content[0],
                        "timestamp": content[1],
                        "part_2": content[2],
                        "content": content[3]
                    }
                    self._extracted_sub_content.append(sub_part)
                else:
                    EMPTY_PATTERN = r'(D.+: \d,)(\d:\d\d:\d\d\.\d{2,3},\d:\d\d:\d\d\.\d{2,3})(,\w+,.*,\d,\d,\d,.*,)$'
                    REGEX_2: Pattern[str] = re.compile(EMPTY_PATTERN)
                    if REGEX_2.match(line):
                        if not remove_empty:
                            content: ASSRegexResults = REGEX_2.findall(line)[0]
                            sub_part: ASSSubPart = {
                                "part_1": content[0],
                                "timestamp": content[1],
                                "part_2": content[2],
                                "content": ''
                            }
                            self._extracted_sub_content.append(sub_part)
                    else:
                        self.info_content.append(line)
            self._extracted_full_content = self._extracted_sub_content

    def create_new_sub_file(self) -> str:
        if CREATE_NEW_FILE:
            filename = f'{self._sub_file_path[:-4]}-NEW.{self._sub_file_path[-3:]}'
        else:
            filename = self._sub_file_path

        with open(filename, 'w', encoding='utf8') as sub_file:
            for info in self.info_content:
                sub_file.write(info)

            for content in self._content_to_write:
                sub = f"{content['part_1']}{content['timestamp']}{content['part_2']}{content['content']}\n"
                sub_file.write(sub)
        return filename