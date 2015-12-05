import numpy as np
import statistics as st
from sklearn import svm

def diff_one_interval(pat, mean, var):
    dim = len(pat)
    for i in range(dim-1):
        if abs(pat[i]-mean[i]) > var:
            return True
    return False

def diff_proportional(pat, var):
    return True if max(pat)-min(pat) > var*2 else False

def diff_normal(pat, mean, var):
    dim = len(pat)
    for i in range(dim):
        if abs(pat[i]-mean[i]) > var:
            return True
    return False

def gen_def_patterns(dim, value, size):
    mean = np.linspace(value, value, dim)
    true_pat = st.gen_samples(dim, mean, size)
    #false_pat = np.random.uniform(value*0.75, value*1.25, (size, dim))
    false_pat = np.random.uniform(value*0.85, value*1.15, (size, dim))
    return mean, true_pat, false_pat

def gen_multi_patterns(dim, value, v1, v2, size):
    mean = np.linspace(value, value, dim)
    m1 = np.linspace(v1, v2, dim)
    m2 = np.linspace(v1, v2, dim)
    true_pat = st.gen_samples(dim, m1, size/2)
    np.append(true_pat, st.gen_samples(dim, m2, size/2), axis=0)
    false_pat = np.random.uniform(value*0.75, value*1.25, (size, dim))
    return mean, true_pat, false_pat

def test_svm(true_pat, false_pat):
    clf = svm.OneClassSVM(nu=0.002, kernel="rbf", gamma=0.1)
    clf.fit(true_pat)
    pred_true = clf.predict(true_pat)
    pred_false = clf.predict(false_pat)
    n_error_true = pred_true[pred_true == -1].size
    n_error_false = pred_false[pred_false == 1].size

    print(n_error_true, pred_true.size)
    print(n_error_false, pred_false.size)
    frr = n_error_true/pred_true.size
    far = n_error_false/pred_false.size

    return far, frr

def var_one_interval(value, var, dim, size, n_test, alg):
    mean, true_pat, false_pat = gen_def_patterns(dim, value, size)
    for pat in true_pat:
        pat[0] = np.random.uniform(value*0.75, value*1.25)
    false_pat = [p for p in false_pat if diff_one_interval(p, mean, var)]
    #print('patterns left for 1 diff: ', len(false_pat))

    if(alg == 'svm'):
        far, frr = test_svm(true_pat, false_pat)

    return

def var_proportional(value, var, dim, size, n_test, alg):
    mean, true_pat, false_pat = gen_def_patterns(dim, value, size)
    for pat in true_pat:
        r = np.random.uniform(value*0.95, value*1.05)
        pat = [p+r for p in pat]
    #dist_pat = [p for p in false_pat if diff_proportional(p, var)]
    #print('patterns left for prop: ', len(dist_pat))
    return

def var_multi_clusters(value, var, dim, size, n_test, alg):
    interval = var*5
    mean, true_pat, false_pat = gen_multi_patterns(dim, value, value-interval, value+interval, size)
    #dist_pat = [p for p in false_pat if diff_normal(p, mean, var)]
    #print('patterns left for multi: ', len(dist_pat))
    return
