from BinaryPso import BinaryPso
import numpy as np


best=np.inf

for i in range(300):
    print(f"iteration={i}")
    b = BinaryPso(size=30, ff_code=2, number_of_decimals=5, iterations=100)
    if b.swarm.gbest_value<best:
        best=b.swarm.gbest_value
        golden_iteration=i

print(f"golden iteration={golden_iteration}")
