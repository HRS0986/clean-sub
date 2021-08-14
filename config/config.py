import json
from typing import List, Optional
from dtypes import Configuration

SETTINGS = (
    ('min', 'MIN_DURATION'),
    ('max', 'MAX_DURATION'),
    ('remove_empty', 'REMOVE_EMPTY'),
    ('new_sub_file', 'CREATE_NEW_FILE'),
    ('keywords', 'KEYWORDS'),
    (None, 'FILE_TYPES')
)


class ConfigHandler:
    """
    This class handle all configuration operations
    """
    def __init__(
            self,
            sub_path: str,                              # Subtitle file path
            filtype: str,                               # Subtitle file type (srt or ass or smi)
            no_empty: bool,                             # Remove empty lines status
            keep_empty: bool,                           # Keep empty lines status
            min_d: Optional[float] = None,              # Minimum display duration to check
            max_d: Optional[float] = None,              # Maximum display duration to check
            script_save_name: Optional[str] = None,     # Settings script save path
            script_name: Optional[str] = None,          # Setting script path to use
            new_file: Optional[bool] = None,            # Create new cleaned subtitle file status
            ext_file: Optional[bool] = None,            # Modify current subtitle file without creating new files status
            keywords_o: Optional[List[str]] = None,     # Keyword to check. Check Only these keywords
            keywords_a: Optional[List[str]] = None,     # Additional keywords to check with default keywords list
            keywords_e: Optional[List[str]] = None      # Exclude these keywords from default keywords list
    ):
        self.filtype = filtype
        self.sub_path = sub_path
        self.__script_save_name = script_save_name
        self.__script_name = script_name
        self.__new_file = new_file
        self.__ext_file = ext_file
        self.__no_empty = no_empty
        self.__keep_empty = keep_empty
        self.__max = max_d
        self.__min = min_d
        self.__keywords_o = keywords_o
        self.__keywords_a = keywords_a
        self.__keywords_e = keywords_e
        self.__default_config_path = r'config/default_config.json'
        self.__config_script_dir = r'config/custom_configurations/'

    def __get_setting(self, setting_name: str) -> Configuration:
        """
        Return a default setting value the from default configuration file
        :param setting_name: Setting name to get the from default configuration file
        :return:
        """
        if self.__script_name:
            script_path = f'{self.__config_script_dir}{self.__script_name}.json'
        else:
            script_path = self.__default_config_path

        with open(script_path, encoding="utf8") as config_file:
            default_settings = json.load(config_file)
        return default_settings.get(setting_name)

    @property
    def min(self):
        if self.__min:
            return self.__min
        return self.__get_setting('MIN_DURATION')

    @property
    def max(self):
        if self.__max:
            return self.__max
        return self.__get_setting('MAX_DURATION')

    @property
    def remove_empty(self):
        if self.__keep_empty:
            return False
        elif self.__no_empty:
            return True
        return self.__get_setting('REMOVE_EMPTY')

    @property
    def new_sub_file(self):
        if self.__new_file:
            return True
        elif self.__ext_file:
            return False
        return self.__get_setting('CREATE_NEW_FILE')

    @property
    def keywords(self):
        KEYWORDS = self.__get_setting('KEYWORDS')
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

    def write_configuration_script(self):
        if self.__script_save_name:
            save_path = f'config/custom_configurations/{self.__script_save_name}.json'
            configurations = {}
            for setting in SETTINGS:
                setting_name = setting[1]
                if setting[0] is not None:
                    setting_value = eval(f'self.{setting[0]}')
                else:
                    setting_value = self.__get_setting(setting_name)
                configurations[setting_name] = setting_value
            with open(save_path, 'w', encoding='utf8') as configuration_file:
                json.dump(configurations, configuration_file, indent=4, ensure_ascii=False)

        else:
            raise Exception('Configuration script path is not provided')
