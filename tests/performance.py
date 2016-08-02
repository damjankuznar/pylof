import time

import numpy as np
from matplotlib import pyplot as plt
import lof

arr = np.genfromtxt("tests/dataset.csv", skip_header=1,
                    dtype=np.float64, delimiter=",")

timings = []
for num_instances in [20, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900,
                      1000]:
    start = time.time()
    l = lof.outliers(10, arr[:num_instances])
    timings.append((num_instances, time.time() - start))

timings = np.array(timings)
print timings.tolist()
plt.plot(timings[:, 0], timings[:, 1])
plt.show()
