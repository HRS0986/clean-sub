import unittest
from clean import CleanSubSRT, CleanSubASS


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
        start = [00, 1, 29, 41]
        end = [00, 1, 30, 458]
        duration: float = self.cleaner_srt._calculate_duration(start, end)
        self.assertEqual(duration, 1.417, msg="Test Calculate Duration Between Start And End")

    def test_split_timeline_srt(self) -> None:
        timestamp = "00:01:29,041 --> 00:01:30,458"
        after_split = {
            'start': [0, 1, 29, 41],
            'end': [0, 1, 30, 458]
        }
        self.assertEqual(self.cleaner_srt._split_timestamp(timestamp), after_split, msg="Test Timestamp Split Of A SRT File")

    def test_split_timeline_ass(self) -> None:
        timestamp = "0:00:01.63,0:00:18.22"
        after_split = {
            'start': [0, 0, 1, 63],
            'end': [0, 0, 18, 22]
        }
        self.assertEqual(self.cleaner_ass._split_timestamp(timestamp), after_split, msg="Test Timestamp Split Of A ASS File")

    # def


if __name__ == '__main__':
    unittest.main()
