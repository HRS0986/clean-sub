from typing import List
from config.default_config import MAX_DURATION, MIN_DURATION, REMOVE_EMPTY, CREATE_NEW_FILE, KEYWORDS
from dtypes import KeywordSet, KeywordStatus


class ConfigHandler:
    def __init__(self, min_d: float = MIN_DURATION, max_d: float = MAX_DURATION, empty: bool = REMOVE_EMPTY,
                 new_file: bool = CREATE_NEW_FILE,
                 keywords: KeywordSet = KEYWORDS):
        self.new_file = new_file
        self.empty = empty
        self.max = max_d
        self.min = min_d
        self.keywords_temp = keywords

    @property
    def keywords(self):
        """
        Allowed statuses:
            additional - add these keywords to default keyword list
            exclude - exclude these keywords to default keyword list
            only - check these keywords only
        """
        if isinstance(self.keywords_temp, dict):
            """
            self.keywords_temp - structure 1
             [
                  {"status": "additional", "keywords": ["test", "r"]}
                  {"status": "exclude", "keywords": ["t", "a"]}
             ]    

             self.keywords_temp - structure 2
             [{"status": "only", "keywords": ["test", "r"]}]
            """

            keywords: List[str] = []
            for key_dict in self.keywords_temp:
                status: KeywordStatus = key_dict['status']
                if status == 'only':
                    return key_dict['keywords']

                elif status == 'additional':
                    keywords.extend(KEYWORDS)
                    keywords.extend(key_dict["keywords"])

                elif status == 'exclude':
                    for keyword in key_dict["keywords"]:
                        keywords.remove(keyword)
            return keywords
        return KEYWORDS

    def write_configuration_script(self, name: str):
        pass
