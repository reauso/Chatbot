import random
import re

from data_handling.reflection import reflect
from data_handling.text_patterns import psychobabble


def patternbased_answer(user_input: str):
    # Test input string for all known text patter in pychobabble
    for pattern, responses in psychobabble:
        match = re.search(pattern.lower(), str(user_input).lower().strip())
        if match:
            answer = random.choice(responses)
            return answer.format(*[reflect(g.strip(",.?!")) for g in match.groups()])
    return None