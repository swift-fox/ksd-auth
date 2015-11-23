from db import Database
from measurement import Measurement
import numpy
from sklearn import svm

class PatternMatch:
    def __init__(self):
        self.db = Database()

    def convert_pattern_to_gaps(self, patterns):
        gaps = []
        for pattern in patterns:
            for i, pat in enumerate(pattern[1:]):
                gaps.append(pat - pattern[i])
        return gaps

    def distance(self, old_pat, new_pat, order):
        old_gaps = self.convert_pattern_to_gaps(old_pat)
        new_gaps = self.convert_pattern_to_gaps(new_pat)
        m = Measurement()
        return m.compute_diff(old_gaps, new_gaps, order)

    def min_dist(self, new_pat, old_pats, order):
        min = None
        for old_pat in old_pats:
            dist = self.distance(new_pat, old_pat, order)
            if min == None or dist < min:
                min = dist
        return min

    def avg_dist(self, new_pat, old_pats, weight, min_limit):
        old_gaps = []
        new_gap = self.convert_pattern_to_gaps(new_pat)
        for pat in old_pats:
            old_gaps.append(self.convert_pattern_to_gaps(pat))
        mean_gap = numpy.mean(old_gaps, axis=0)
        std_gap = numpy.std(old_gaps, axis=0)
        limit = numpy.linalg.norm(std_gap)
        if limit < min_limit: limit = min_limit
        dist = numpy.linalg.norm(mean_gap-new_gap)
        return True if weight*limit > dist else False

    def svm_novelty(self, new_pat, old_pats):
        old_gaps = []
        new_gap = self.convert_pattern_to_gaps(new_pat)
        for pat in old_pats:
            old_gaps.append(self.convert_pattern_to_gaps(pat))
        clf = svm.OneClassSVM(kernel="linear")
        clf.fit(old_gaps)
        pred = clf.predict([new_gap])
        return True if pred[0] == 1 else False

    def is_similar(self, new_pat, old_pats, method):
        ret = False
        if(method == 'MAN_DIST'):
            threshold = 0.1
            dist = self.min_dist(new_pat, old_pats, 1)
            print('distance = ', dist)
            ret = True if dist < threshold else False
        elif(method == 'EUC_DIST'):
            threshold = 0.1
            dist = self.min_dist(new_pat, old_pats, 2)
            print('distance = ', dist)
            ret = True if dist < threshold else False
        elif(method == 'MEAN_STD'):
            weight = 1.0
            return self.avg_dist(new_pat, old_pats, weight, 0.4)
        elif(method == 'SVM'):
           return self.svm_novelty(new_pat, old_pats)
        else:
            print('The method is not defined')

        return ret

    def compute_pattern(self, username, password, new_pat):
        db = Database()
        if db.exist_user() == False:
            pass # return authentication failed message

        old_pats = db.read_patterns(username)
        if self.compare_patterns(new_pat, old_pats) == True:
            db.add_pattern(username, new_pat)
        else:
            pass # return invalid pattern
