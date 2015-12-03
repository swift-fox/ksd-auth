import numpy as np
import scipy.spatial.distance as dist
import matplotlib.pyplot as plt
from random import gauss

def make_rand_vector(dims, min_v, max_v):
    vec = [gauss(min_v, max_v) for i in range(dims)]
    mag = sum(x**2 for x in vec) ** .5
    return [x/mag for x in vec]

def gen_uni_random(dim, v_dur, v_int, size):
    r_int = np.random.uniform(0, v_int*2, size)
    r_dur = np.random.uniform(0, v_dur*2, size)
    r_pat = []
    for pat in range(size):
        pat = np.linspace(0, 0, dim*2)
        for i in range(dim):
            pat[i*2] = r_int[i]
            pat[i*2+1] = r_dur[i]
        r_pat.append(pat)
    return r_pat

def gen_gauss_random(mean, cov, size):
    dim = len(mean)
    return np.random.multivariate_normal(mean, cov, size)

def gen_samples(mean, size):
    dim = len(mean)
    var = (mean*0.1)
    cov = np.outer(var, var)
    return gen_gauss_random(mean, cov, size)

def gen_data(dim, v_dur, v_int, size):
    m_dur = np.linspace(v_dur, v_dur, dim)
    m_int = np.linspace(v_int, v_int, dim)
    mean = np.linspace(0, 0, dim*2)
    for i in range(dim):
        mean[i*2] = m_dur[i]
        mean[i*2+1] = m_int[i]
    pat = gen_samples(mean, size)
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
    n_samples = 1000
    dim = 10
    v_dur = 0.1
    v_int = 0.2
    data = gen_data(dim, v_dur, v_int, n_samples)
    draw_plot(data)
    #fake_data = gen_uni_random(dim, v_dur, v_int, n_samples)
    #draw_plot(fake_data)