import numpy as np
import statistics as st
from sklearn import svm
import scipy.spatial.distance as dist
from sklearn.neighbors import NearestNeighbors

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

def gen_def_patterns(dim, value, var, size, method):
    mean = np.linspace(value, value, dim)
    if method == 'one':
        true_pat = st.gen_samples(dim, mean, var, size)
        false_pat = np.random.uniform(value-(var*3), value+(var*3), (size, dim))
        #false_pat = np.random.uniform(value*0.85, value*1.15, (size, dim))
        for pat in true_pat:
            pat[0] = np.random.uniform(value*0.75, value*1.25)
    elif method == 'prop':
        true_pat = st.gen_samples(dim, mean, var, size)
        false_pat = np.random.uniform(value-(var*3), value+(var*3), (size, dim))
        #false_pat = np.random.uniform(value*0.85, value*1.15, (size, dim))
        for pat in true_pat:
            r = np.random.uniform(value*0.95, value*1.05)
            pat = [p+r for p in pat]
    elif method == 'multi':
        interval = var*5
        v1 = value - interval
        v2 = value + interval
        m1 = np.linspace(v1, v2, dim)
        m2 = np.linspace(v1, v2, dim)
        true_pat = st.gen_samples(dim, m1, var, size/2)
        np.append(true_pat, st.gen_samples(dim, m2, var, size/2), axis=0)
        false_pat = np.random.uniform(value+(var*3), value-(var*3), (size, dim))
    else:
        print 'Not supported method'

    return mean, true_pat, false_pat

def test_euc_dist(true_pat, false_pat, err_bound):
    n_error_true = 0
    n_error_false = 0
    nbrs = NearestNeighbors(n_neighbors=2, algorithm='auto').fit(true_pat)
    for i, t_pat in enumerate(true_pat):
        #dist_pairs = [dist.euclidean(t_pat, p) for j, p in enumerate(true_pat) if i is not j]
        #min_dist = min(dist_pairs)
        d, idx = nbrs.kneighbors([t_pat])
        min_dist = d[0][1]
        if(min_dist > err_bound):
            n_error_true += 1
    for f_pat in false_pat:
        #dist_pairs = [dist.euclidean(f_pat, p) for p in true_pat]
        #min_dist = min(dist_pairs)
        d, idx = nbrs.kneighbors([f_pat], n_neighbors=1)
        min_dist = d[0][0]
        if(min_dist < err_bound):
            n_error_false += 1
    frr = float(n_error_true)/float(len(true_pat))
    far = float(n_error_false)/float(len(false_pat))
    return far, frr

def test_mah_dist(true_pat, false_pat, err_bound):
    n_error_true = 0
    n_error_false = 0
    for i, t_pat in enumerate(true_pat):
        ex_pat = [p for j, p in enumerate(true_pat) if i is not j]
        m = np.mean(ex_pat, axis=0)
        cov = np.cov(ex_pat, rowvar=0)
        inv_cov = np.linalg.pinv(cov)
        mah_dist = dist.mahalanobis(t_pat, m, inv_cov)
        if(mah_dist > err_bound):
            n_error_true += 1

    m = np.mean(true_pat, axis=0)
    cov = np.cov(true_pat, rowvar=0)
    inv_cov = np.linalg.pinv(cov)
    for f_pat in false_pat:
        mah_dist = dist.mahalanobis(f_pat, m, inv_cov)
        if(mah_dist < err_bound):
            n_error_false += 1

    frr = float(n_error_true)/float(len(true_pat))
    far = float(n_error_false)/float(len(false_pat))
    return far, frr

def test_svm(true_pat, false_pat):
    clf = svm.OneClassSVM(nu=0.1)
    clf.fit(true_pat)
    pred_true = clf.predict(true_pat)
    pred_false = clf.predict(false_pat)
    n_error_true = pred_true[pred_true == -1].size
    n_error_false = pred_false[pred_false == 1].size

    #print(n_error_true, pred_true.size)
    #print(n_error_false, pred_false.size)
    frr = float(n_error_true)/float(pred_true.size)
    far = float(n_error_false)/float(pred_false.size)

    return far, frr

#euc_factor = 0.15
euc_bound = 0.05
mah_bound = 2.5

def compute_error_rate(true_pat, false_pat, n_test, alg):
    if(alg == 'euc'):
        far, frr = test_euc_dist(true_pat, false_pat, euc_bound)
    elif(alg == 'mah'):
        far, frr = test_mah_dist(true_pat, false_pat, mah_bound)
    elif(alg == 'svm'):
        far, frr = test_svm(true_pat, false_pat)
    else:
        print('Not supported algorithm')
        return 0, 0

    return far, frr

def var_interval(plt, value, vars, dim, size, n_test, pvar):
    plt.figure()
    euc_fars, euc_frrs, mah_fars, mah_frrs, svm_fars, svm_frrs = [], [], [], [], [], []
    for var in vars:
        mean, true_pat, false_pat = gen_def_patterns(dim, value, var, size, pvar)
        for pat in true_pat:
            pat[0] = np.random.uniform(value-(var*3), value+(var*3))
        sum_far, sum_frr = 0.0, 0.0
        for i in range(n_test):
            euc_far, euc_frr = compute_error_rate(true_pat, false_pat, n_test, 'euc')
            sum_far += euc_far
            sum_frr += euc_frr
        avg_far = sum_far / n_test
        avg_frr = sum_frr / n_test
        print(avg_far, avg_frr)
        euc_fars.append(avg_far)
        euc_frrs.append(avg_frr)

        sum_far, sum_frr = 0.0, 0.0
        for i in range(n_test):
            euc_far, euc_frr = compute_error_rate(true_pat, false_pat, n_test, 'mah')
            sum_far += euc_far
            sum_frr += euc_frr
        avg_far = sum_far / n_test
        avg_frr = sum_frr / n_test
        print(avg_far, avg_frr)
        mah_fars.append(avg_far)
        mah_frrs.append(avg_frr)

        sum_far, sum_frr = 0.0, 0.0
        for i in range(n_test):
            euc_far, euc_frr = compute_error_rate(true_pat, false_pat, n_test, 'svm')
            sum_far += euc_far
            sum_frr += euc_frr
        avg_far = sum_far / n_test
        avg_frr = sum_frr / n_test
        print(avg_far, avg_frr)
        print()
        svm_fars.append(avg_far)
        svm_frrs.append(avg_frr)

    plt.xlabel('Standard deviation')
    plt.ylabel('Error Rate')
    efar, = plt.plot(vars, euc_fars, color='red', label='FAR(NN)')
    efrr, = plt.plot(vars, euc_frrs, color='red', label='FRR(NN)', linestyle='--')
    mfar, = plt.plot(vars, mah_fars, color='green', label='FAR(Mahalanobis)')
    mfrr, = plt.plot(vars, mah_frrs, color='green', label='FRR(Mahalanobis)', linestyle='--')
    sfar, = plt.plot(vars, svm_fars, color='blue', label='FAR(SVMs)')
    sfrr, = plt.plot(vars, svm_frrs, color='blue', label='FRR(SVMs)', linestyle='--')
    plt.legend(handles=[efar, efrr, mfar, mfrr, sfar, sfrr], loc='upper left')
    return

'''
def var_proportional(plt, value, vars, dim, size, n_test):
    plt.figure()
    euc_fars, euc_frrs, mah_fars, mah_frrs, svm_fars, svm_frrs = [], [], [], [], [], []
    for var in vars:
        sum_far, sum_frr = 0.0, 0.0
        for i in range(n_test):
            mean, true_pat, false_pat = gen_def_patterns(dim, value, var, size, 'prop')
            for pat in true_pat:
                pat[0] = np.random.uniform(value-(var*3), value+(var*3))
            euc_far, euc_frr = compute_error_rate(true_pat, false_pat, n_test, 'euc')
            sum_far += euc_far
            sum_frr += euc_frr
        avg_far = sum_far / n_test
        avg_frr = sum_frr / n_test
        #print(avg_far, avg_frr)
        euc_fars.append(avg_far)
        euc_frrs.append(avg_frr)

        sum_far, sum_frr = 0.0, 0.0
        for i in range(n_test):
            mean, true_pat, false_pat = gen_def_patterns(dim, value, var, size, 'prop')
            for pat in true_pat:
                pat[0] = np.random.uniform(value-(var*3), value+(var*3))
            euc_far, euc_frr = compute_error_rate(true_pat, false_pat, n_test, 'mah')
            sum_far += euc_far
            sum_frr += euc_frr
        avg_far = sum_far / n_test
        avg_frr = sum_frr / n_test
        #print(avg_far, avg_frr)
        mah_fars.append(avg_far)
        mah_frrs.append(avg_frr)

        sum_far, sum_frr = 0.0, 0.0
        for i in range(n_test):
            mean, true_pat, false_pat = gen_def_patterns(dim, value, var, size*10, 'prop')
            for pat in true_pat:
                pat[0] = np.random.uniform(value-(var*3), value+(var*3))
            euc_far, euc_frr = compute_error_rate(true_pat, false_pat, n_test, 'svm')
            sum_far += euc_far
            sum_frr += euc_frr
        avg_far = sum_far / n_test
        avg_frr = sum_frr / n_test
        #print(avg_far, avg_frr)
        svm_fars.append(avg_far)
        svm_frrs.append(avg_frr)

    return

def var_multi_clusters(plt, value, var, dim, size, n_test):
    plt.figure()
    interval = var*5
    sum_far, sum_frr = 0.0, 0.0
    for i in range(n_test):
        mean, true_pat, false_pat = gen_multi_patterns(dim, value, value-interval, value+interval, var, size)
        for pat in true_pat:
            pat[0] = np.random.uniform(value-(var*3), value+(var*3))
        euc_far, euc_frr = compute_error_rate(true_pat, false_pat, n_test, 'euc')
        sum_far += euc_far
        sum_frr += euc_frr
    avg_far = sum_far / n_test
    avg_frr = sum_frr / n_test
    print(avg_far, avg_frr)

    sum_far, sum_frr = 0.0, 0.0
    for i in range(n_test):
        mean, true_pat, false_pat = gen_multi_patterns(dim, value, value-interval, value+interval, var, size)
        for pat in true_pat:
            pat[0] = np.random.uniform(value-(var*3), value+(var*3))
        euc_far, euc_frr = compute_error_rate(true_pat, false_pat, n_test, 'mah')
        sum_far += euc_far
        sum_frr += euc_frr
    avg_far = sum_far / n_test
    avg_frr = sum_frr / n_test
    print(avg_far, avg_frr)

    sum_far, sum_frr = 0.0, 0.0
    for i in range(n_test):
        mean, true_pat, false_pat = gen_multi_patterns(dim, value, value-interval, value+interval, var, size*10)
        for pat in true_pat:
            pat[0] = np.random.uniform(value-(var*3), value+(var*3))
        euc_far, euc_frr = compute_error_rate(true_pat, false_pat, n_test, 'svm')
        sum_far += euc_far
        sum_frr += euc_frr
    avg_far = sum_far / n_test
    avg_frr = sum_frr / n_test
    print(avg_far, avg_frr)

    return
'''
