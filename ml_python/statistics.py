import numpy as np
import scipy.spatial.distance as dist
import matplotlib.pyplot as plt
import test
from random import gauss

def make_rand_vector(dims, min_v, max_v):
    vec = [gauss(min_v, max_v) for i in range(dims)]
    mag = sum(x**2 for x in vec) ** .5
    return [x/mag for x in vec]

def gen_samples(dim, mean, size):
    var = (mean * 0.1)**2
    cov = np.outer(var, var)
    return np.random.multivariate_normal(mean, cov, size)

def gen_data(dim, value, size):
    mean = np.linspace(value, value, dim)
    pat = gen_samples(dim, mean, size)
    d = []
    for i, p in enumerate(pat):
        d.append(dist.euclidean(mean, p))
    return d

def draw_plot(data):
    count, bins, ignored = plt.hist(data, 50)
    plt.xlabel('Distnace')
    plt.ylabel('Patterns')
    plt.title('Pattern distribution')
    plt.show()

if __name__ == '__main__':
    n_samples = 10000
    dim = 19
    value = 0.1
    var = value * 0.1
    mean = np.linspace(value, value, dim)
    n_test = 100
    #data = gen_data(dim, value, n_samples)
    #draw_plot(data)
    false_pat = np.random.uniform(value*0.75, value*1.25, (n_samples, dim))
    #draw_plot(fake_data)
    test.var_one_interval(value, var, dim, n_samples, n_test, 'svm')
    test.var_proportional(value, var, dim, n_samples, n_test, 'svm')
    test.var_multi_clusters(value, var, dim, n_samples, n_test, 'svm')
