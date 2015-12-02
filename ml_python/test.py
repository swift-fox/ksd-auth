import numpy as np
import scipy.spatial.distance as dist
import matplotlib.pyplot as plt

def gen_random(mean, cov, size):
    dim = len(mean)
    return np.random.multivariate_normal(mean, cov, size)

def gen_samples(mean):
    dim = len(mean)
    var = (mean*0.1)
    cov = np.outer(var, var)
    return gen_random(mean, cov, n_samples)

if __name__ == '__main__':
    n_samples = 100000
    dim = 10
    v_dur = 0.1
    v_int = 0.2
    m_dur = np.linspace(v_dur, v_dur, dim)
    m_int = np.linspace(v_int, v_int, dim)
    mean = np.linspace(0, 0, dim*2)
    for i in range(dim):
        mean[i*2] = m_dur[i]
        mean[i*2+1] = m_int[i]

    pat = gen_samples(mean)
    d = []
    for i, p in enumerate(pat):
        d.append(dist.euclidean(mean, p))

    count, bins, ignored = plt.hist(d, 50)
    plt.xlabel('Distnace')
    plt.ylabel('Patterns')
    plt.title('Pattern distribution')
    plt.show()