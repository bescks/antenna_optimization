import numpy as np

A = np.arange(12).reshape((3, 4))
print(np.split(A, 2, axis=1))
