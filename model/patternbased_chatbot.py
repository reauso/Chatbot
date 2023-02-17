import random
import re

from data_handling.reflection import reflect
from data_handling.util import read_jsonfile


class PatternBasedChatbot:
    def __init__(self, pattern_file):
        # Test input string for all known text patter in pychobabble
        self.psychobabble = read_jsonfile(pattern_file)

    def __call__(self, request):
        for pattern, responses in self.psychobabble:
            match = re.search(pattern.lower(), str(request).lower().strip())
            if match:
                answer = random.choice(responses)
                return answer.format(*[reflect(g.strip(",.?!")) for g in match.groups()])

        return None
