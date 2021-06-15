import unittest
from clean import CleanSubSRT, CleanSubASS
from mock_data import MOCK_DATA
from typing import List, Dict


class TestCleanSub(unittest.TestCase):
    def setUp(self) -> None:
        self.cleaner_srt = CleanSubSRT('D.srt')
        self.cleaner_ass = CleanSubASS('L.ass')

    def test_cleaner_filetype(self) -> None:
        srt_filetype = self.cleaner_srt.filetype
        ass_filetype = self.cleaner_ass.filetype
        self.assertEqual(srt_filetype, 'srt', msg="Test SRT Filetype")
        self.assertEqual(ass_filetype, 'ass', msg="Test ASS Filetype")

    def test_calculate_duration(self) -> None:
        timelines: List[Dict] = MOCK_DATA['durations']
        for timeline in timelines:
            start = timeline['start']
            end = timeline['end']
            expected_duration = timeline['duration']
            duration: float = self.cleaner_srt._calculate_duration(start, end)
            self.assertEqual(expected_duration, duration, msg="Test Calculate Duration Between Start And End")

    def test_split_timeline_srt(self) -> None:
        timestamp = "00:01:29,041 --> 00:01:30,458"
        after_split = {
            'start': [0, 1, 29.041],
            'end': [0, 1, 30.458]
        }
        self.assertEqual(after_split, self.cleaner_srt._split_timestamp(timestamp), msg="Test Timestamp Split Of A SRT File")

    def test_split_timeline_ass(self) -> None:
        timestamp = "0:00:01.63,0:00:18.22"
        after_split = {
            'start': [0, 0, 1.63],
            'end': [0, 0, 18.22]
        }
        self.assertEqual(self.cleaner_ass._split_timestamp(timestamp), after_split, msg="Test Timestamp Split Of A ASS File")

    def test_detect_by_duration(self) -> None:
        self.cleaner_srt._extracted_sub_content = MOCK_DATA['srt_timestamp']
        self.cleaner_srt.detect_unwanted_by_duration()
        expected_to_write = MOCK_DATA['srt_content_to_write']
        expected_removed = MOCK_DATA['srt_timestamp_expected_duration']
        removed_count = len(self.cleaner_srt._unwanted_content)
        write_count = len(self.cleaner_srt._extracted_sub_content)
        for content in expected_removed:
            self.assertIn(content, self.cleaner_srt._unwanted_content, msg="Test Removed Contents By Duration")
        for content in expected_to_write:
            self.assertIn(content, self.cleaner_srt._extracted_sub_content, msg="Test Contents After Removed")
        self.assertEqual(len(expected_removed), removed_count, msg="Test Removed Content Count")
        self.assertEqual(len(expected_to_write), write_count, msg="Test To Write Content Count")

    def test_remove_unwanted(self) -> None:
        expected_content = MOCK_DATA['srt_content_to_write']
        to_remove = MOCK_DATA['srt_timestamp_expected_duration']
        self.cleaner_srt._extracted_full_content = MOCK_DATA['srt_timestamp']
        self.cleaner_srt.remove_unwanted(to_remove)
        expected_count = len(expected_content)
        actual_count = len(self.cleaner_srt._content_to_write)
        for content in expected_content:
            self.assertIn(content, self.cleaner_srt._content_to_write, msg="Test Remove Unwanted Content")
        self.assertEqual(expected_count, actual_count, msg="Test Remove Unwanted Content Count")


if __name__ == '__main__':
    unittest.main()
