import re
from typing import Pattern
from config import MIN_DURATION, MAX_DURATION, KEYWORDS, CREATE_NEW_FILE


class CleanSub:

    def __init__(self, sub_file_path: str):
        self.__sub_file_path = sub_file_path
        self.__extracted_sub_content: list[dict] = []
        self.__extracted_full_content: list[dict] = []
        self.unwanted_content = []
        self.__content_to_write = []

    def __str__(self):
        pass

    def extract_subtitles(self) -> None:
        with open(self.__sub_file_path, 'r', encoding='utf8') as sub_file:
            sub_content: str = sub_file.read()
            SUB_PATTERN = r'([0-9]+\n.+(\n.+){1,})'
            REGEX: Pattern[str] = re.compile(SUB_PATTERN)
            results: list[tuple] = REGEX.findall(sub_content)
            for result_group in results:
                lines = result_group[0].split('\n')
                number = lines[0]
                timestamp = lines[1]
                sub = lines[2:]
                sub_part = {
                    'number': number,
                    'timestamp': timestamp,
                    'content': sub
                }
                self.__extracted_sub_content.append(sub_part)
            self.__extracted_full_content = self.__extracted_sub_content

    def detect_unwanted_by_content(self):
        # Check content has specific words
        after_content = []
        i = 0
        for content in self.__extracted_sub_content:
            i += 1
            sub_content = ' '.join(content['content'])
            for keyword in KEYWORDS:
                if keyword in sub_content:
                    self.unwanted_content.append(content)
                    break
            else:
                after_content.append(content)
        self.__extracted_sub_content = after_content

    def _split_timestamp(self, timestamp: str) -> dict:
        start, end = timestamp.split(' --> ')
        sh, sm, ss = start.split(':')
        ss, sms = ss.split(',')
        eh, em, es = end.split(':')
        es, ems = es.split(',')
        return {'start': [int(sh), int(sm), int(ss), int(sms)], 'end': [int(eh), int(em), int(es), int(ems)]}

    def _calculate_duration(self, start: list[int], end: list[int]) -> float:
        duration = 0.000
        if end[-1] < start[-1]:
            end[-1] += 1000
            end[-2] -= 1
        duration += (end[-1] - start[-1]) / 1000

        if end[-2] < start[-2]:
            end[-2] += 60
            end[1] -= 1
        duration += end[-2] - start[-2]
        duration = float(f'{duration:.3f}')
        return duration

    def detect_unwanted_by_duration(self):
        after_duration = []
        for content in self.__extracted_sub_content:
            split_timestamp: dict[str, list[int]] = self._split_timestamp(content['timestamp'])
            start = split_timestamp['start']
            end = split_timestamp['end']
            duration = self._calculate_duration(start, end)
            if duration <= MIN_DURATION:
                self.unwanted_content.append(content)
            elif duration >= MAX_DURATION:
                self.unwanted_content.append(content)
            else:
                after_duration.append(content)
        self.__extracted_sub_content = after_duration

    def remove_unwanted(self, content_numbers: tuple[int, ...]):
        if content_numbers[0] == 0:
            self.__content_to_write = self.__extracted_sub_content
        else:
            exclude_from_new: list[dict] = [self.unwanted_content[i-1] for i in content_numbers]
            for content in self.__extracted_full_content:
                if content in exclude_from_new:
                    exclude_from_new.remove(content)
                    continue
                self.__content_to_write.append(content)

    def create_new_sub_file(self) -> str:
        if CREATE_NEW_FILE:
            filename = f'{self.__sub_file_path[:-4]}-NEW.{self.__sub_file_path[-3:]}'
        else:
            filename = self.__sub_file_path

        with open(filename, 'w', encoding='utf8') as sub_file:
            for content in self.__content_to_write:
                sub = f"{content['number']}\n{content['timestamp']}\n{content['content']}\n\n"
                sub_file.write(sub)
        return filename
