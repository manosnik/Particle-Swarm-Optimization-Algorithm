import numpy as np
from numpy import array as arr
import random
import math


class Particle:

    def __init__(self, id, dim, bound_min, bound_max, v_max):
        self.id = id
        self.dim = dim
        self.bound_min = bound_min
        self.bound_max = bound_max
        self.v_max = v_max
        self.fitness_value = None
        self.fitness_value_p_best = np.inf
        self.v_next = np.empty(self.dim, dtype=float)
        self.x = np.empty(self.dim, dtype=float)

        for i in range(self.dim):
            self.x[i] = np.random.uniform(self.bound_min[i], self.bound_max[i])

        self.v = np.empty(self.dim, dtype=float)
        for i in range(self.dim):
            self.v[i] = np.random.uniform(-self.v_max[i], self.v_max[i])

        self.p_best = self.x

    def __str__(self):
        return f"{self.id}{self.x}{self.v}{self.p_best}"

    def upgrade_vel(self, w, c1, c2, g_best):
        self.v_next = w * self.v + c1 * random.random() * (self.p_best - self.x) + c2 * random.random() * (
                g_best - self.x);
        for i in range(self.dim):
            if self.v_next[i] > self.v_max[i]:
                self.v_next[i] = self.v_max[i]
            elif self.v_next[i] < -self.v_max[i]:
                self.v_next[i] = -self.v_max[i]
        return

    def upgrade_position(self):
        self.x = self.x + self.v_next
        for i in range(self.dim):
            if self.x[i] > self.bound_max[i]:
                self.x[i] = self.bound_max[i]
            elif self.x[i] < self.bound_min[i]:
                self.x[i] = self.bound_min[i]

    def upgrade_pbest(self):

        if (self.fitness_value < self.fitness_value_p_best):
            self.p_best = self.x
            self.fitness_value_p_best = self.fitness_value
        return

    def fitness_function(self):
        # burkin 6
        print(f"{self.x}")

        term1 = 100 * math.sqrt(abs(self.x[1] - 0.01 * self.x[0] ** 2))
        term2 = 0.01 * abs(self.x[0] + 10)

        self.fitness_value = term1 + term2
        print(f"{self.x} {self.fitness_value}")
        return




# eggholder

# a = math.sqrt(math.fabs(self.x[1] + self.x[0] / 2 + 47))
# b = math.sqrt(math.fabs(self.x[0] - (self.x[1] + 47)))
# self.fitness_value = -(self.x[1] + 47) * math.sin(a) - self.x[0] * math.sin(b)
# return

# frastring
# d = len(self.x)
# sum = 0
#
# for i in self.x:
#     sum += (i ** 2 - 10 * math.cos(2 * math.pi * i))
#
# y = 10 * d + sum
# self.fitness_value=y
# return
