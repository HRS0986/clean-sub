from typing import List, Dict, Tuple, Union

ContentList = List[Dict[str, Union[str, List[str]]]]
SplitTimestamp = Dict[str, List[Union[int, float]]]
SRTSubPart = Dict[str, Union[str, List[str]]]
ASSSubPart = Dict[str, str]
SRTRegexResults = List[Tuple[str, str]]
ASSRegexResults = Tuple[str, str, str, str]
