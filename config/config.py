from typing import List, Optional
from config.default_config import MAX_DURATION, MIN_DURATION, REMOVE_EMPTY, CREATE_NEW_FILE, KEYWORDS


class ConfigHandler:
    def __init__(
            self,
            sub_path: str,
            filtype: str,
            min_d: float = MIN_DURATION,
            max_d: float = MAX_DURATION,
            empty: bool = REMOVE_EMPTY,
            script_path: Optional[str] = None,
            new_file: Optional[bool] = None,
            ext_file: Optional[bool] = None,
            keywords_o: Optional[List[str]] = None,
            keywords_a: Optional[List[str]] = None,
            keywords_e: Optional[List[str]] = None
    ):
        self.__script_path = script_path
        self.filtype = filtype
        self.__new_file = new_file
        self.__ext_file = ext_file
        self.sub_path = sub_path
        self.empty = empty
        self.max = max_d
        self.min = min_d
        self.__keywords_o = keywords_o
        self.__keywords_a = keywords_a
        self.__keywords_e = keywords_e

    @property
    def new_sub_file(self):
        if self.__new_file:
            return True
        elif self.__ext_file:
            return False
        return CREATE_NEW_FILE

    @property
    def keywords(self):
        keywords = [*KEYWORDS]
        if self.__keywords_o:
            return self.__keywords_o

        if self.__keywords_a:
            additional_keywords = ' '.join(self.__keywords_a).split(',')
            keywords.extend(additional_keywords)

        if self.__keywords_e:
            exclude_keywords = ' '.join(self.__keywords_e).split(',')
            for keyword in exclude_keywords:
                keywords.remove(keyword)
        return keywords

    def write_configuration_script(self, script_path: str):
        pass
