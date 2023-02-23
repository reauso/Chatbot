import random
import re

from data_handling.reflection import reflect
from data_handling.util import read_jsonfile
from memory import add_user_name


class PatternBasedChatbot:
    def __init__(self, pattern_file):
        # Test input string for all known text patter in pychobabble
        self.psychobabble = read_jsonfile(pattern_file)

    def __call__(self, request):
        for pattern, responses in self.psychobabble:
            match = re.search(pattern.lower(), str(request).lower().strip())
            if match:
                answer = random.choice(responses)
                if re.search("(my name is|I,'m)\\s+(.*)\\s*\\.?", str(request).lower().strip()):
                    add_user_name(re.sub("(my name is|I,'m)\\s+(.*)\\s*\\.?", '', request))
                return answer.format(*[reflect(g.strip(",.?!")) for g in match.groups()])

        return None
