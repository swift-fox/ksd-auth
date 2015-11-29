import math
import config

def match(pattern, model):
    _pattern = pattern[0] + pattern[1]
    _model = model[0] + model[1]

    diff = 0
    for p, m in zip(_pattern, _model):
        diff += math.fabs(p - m)

    if len(model[0]):
        diff /= len(model[0])

    return (diff < config.matching_error_thresh, diff)

def train(dataset):
    press = [0] * len(dataset[0][0])
    release = [0] * len(dataset[0][1])

    for pattern in dataset:
        press = [a + b for a, b in zip(pattern[0], press)]
        release = [a + b for a, b in zip(pattern[1], release)]

    press = [x / len(dataset) for x in press]
    release = [x / len(dataset) for x in release]

    return (press, release)
