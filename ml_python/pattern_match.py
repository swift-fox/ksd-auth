from db import Database
from measurement import Measurement

class PatternMatch:
    def __init__(self):
        self.db = Database()
    def convert_pattern_to_gaps(self, pattern):
        gaps = []
        for i, pat in enumerate(pattern[1:]):
            gaps.append(pat - pattern[i-1])
        return gaps

    def compare_gaps(self, old_pat, new_pat):
        old_gaps = self.convert_pattern_to_gaps(old_pat)
        new_gaps = self.convert_pattern_to_gaps(new_pat)
        m = Measurement()
        return m.compute_diff(old_gaps, new_gaps, 2)

    def min_dist(self, patterns):
        min_press = None
        min_release = None
        new_pair = patterns[-1]
        for old_pair in patterns[:-1]:
            dist_press = self.compare_gaps(new_pair[0], old_pair[0])
            dist_release = self.compare_gaps(new_pair[1], old_pair[1])
            if min_press == None or dist_press < min_press:
                min_press = dist_press
            if min_release == None or dist_release < min_release:
                min_release = dist_release
        return (min_press + min_release) / 2

    def register_user(self, username, password):
        self.db = Database()
        self.db.add_user(username, password)

    def compute_pattern(self, username, password, new_pat):
        db = Database()
        if db.exist_user() == False:
            pass # return authentication failed message

        old_pats = db.read_patterns(username)
        if self.compare_patterns(new_pat, old_pats) == True:
            db.add_pattern(username, new_pat)
        else:
            pass # return invalid pattern
