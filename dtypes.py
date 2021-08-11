from typing import List, Dict, Mapping, Tuple, Union, Literal, Optional

ContentList = List[Mapping[str, Union[str, List[str]]]]
SplitTimestamp = Dict[str, List[Union[int, float]]]
SRTSubPart = Dict[str, Union[str, List[str]]]
ASSSubPart = Dict[str, str]
SMISubPart = Dict[str, str]
SRTRegexResults = List[Tuple[str, str]]
ASSRegexResults = Tuple[str, str, str, str]
SMIRegexResults = List[Tuple[str, str, str]]
Configuration = Optional[Union[str, bool, float, List[str]]]
