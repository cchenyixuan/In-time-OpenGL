import numpy as np
from PIL import Image
import csv
from multiprocessing import Pool


def g(x, t):
    if type(x) == float or type(x) == int:
        x = np.array([x])
    return 1/(4 * np.pi * t) * np.exp(-x @ x / (4 * t))


def worker(t):

    ans = np.zeros([801, 801], np.float32)
    for i in range(ans.shape[0]):
        for j in range(ans.shape[1]):
            x = np.array([(i - 400) / 100, (j - 400) / 100], dtype=np.float32)
            ans[i, j] = g(x, t)

    output = []
    for i in range(ans.shape[0]):
        for j in range(ans.shape[1]):
            vertex = [(i - 400) / 100, (j - 400) / 100, ans[i, j], t, t, t]
            output.append(vertex)

    return np.array(output)


if __name__ == '__main__':
    pool = Pool()
    arguments = [i * 0.001 for i in range(1, 101)]
    data = pool.map(worker, arguments)
    data = np.array(data, dtype=np.float32)
    np.save("data.npy", data)
