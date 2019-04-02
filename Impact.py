from enum import Enum


class Impact(Enum):
    BLOCKER = -2
    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1
    PERFECT = 2
