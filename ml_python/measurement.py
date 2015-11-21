from math import*
from decimal import Decimal

class Measurement:
    def nth_root(self, value, n_root):
        root_value = 1/float(n_root)
        return round (Decimal(value) ** Decimal(root_value),3)

    def compute_diff(self, old_arr, new_arr, p_value):
        return self.nth_root(sum(pow(abs(a-b), p_value) for a, b in zip(old_arr, new_arr)), p_value)

    def is_similar(self, old_arr, new_arr):
        if self.compute_diff(self, old_arr, new_arr, 2) < self.threshold:
            return True
        else:
            return False

