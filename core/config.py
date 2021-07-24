from typing import Final, Tuple

# Minimum display duration of a subtitle to check
MIN_DURATION: Final[float] = 0.5

# Maximum display duration of a subtitle to check
MAX_DURATION: Final[int] = 7

# Words to check in a subtitle
KEYWORDS: Final[Tuple[str, ...]] = (
    'උපසිරැසි',
    'උපසිරසි',
    'උපසිරස',
    'උපසිරැස',
    'පරිවර්තන අයිතිය සුරකින්න',
    'ඉෂාන් කොම්',
    'SUBZLK',
    'subzlk',
    'SubzLK',
    'SUBZ.LK',
    'Subs.lk',
    'subz.lk',
    "cineru.lk",
    "Cineru.lk",
    'Upasirasi.com',
    'upasirasi.com',
    'PirateLk.Com',
    'pirateLk.Com',
    'piratelk.Com',
    'baiscopelk.com',
    'Baiscopelk.com',
    'BaiscopeLK.com',
    'BaiscopeLk.com',
    'www.',
    'WWW.',
    '\pos',
    'c&H',
    '<font color=',
)

# Create new subtitle file or modify the current subtitle file
CREATE_NEW_FILE: Final[bool] = False

# Remove Empty Subtitle Lines. Only For .ass Files
REMOVE_EMPTY: Final[bool] = True

# Supported File Types
FILE_TYPES: Final[Tuple[str, ...]] = ('ass', 'smi', 'srt')
