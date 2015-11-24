'''
Measure distance between two points and normalize
'''
from math import*
from decimal import Decimal

class Measurement:
    def nth_root(self, value, n_root):
        root_value = 1/float(n_root)
        return round (Decimal(value) ** Decimal(root_value),3)

    def compute_diff(self, old_arr, new_arr, p_value):
        size = len(old_arr)
        return self.nth_root(sum(pow(abs(a-b), p_value) for a, b in zip(old_arr, new_arr))/size, p_value)


