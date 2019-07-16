import numpy as np
from scipy.spatial.distance import euclidean

from fastdtw import fastdtw

x = np.array([22, 22, 25, 28, 67, 144, 53, 20])
y = np.array([144, 170, 74, 66, 168, 526, 210, 61])
distance, path = fastdtw(x, y, dist=euclidean)
print(distance)