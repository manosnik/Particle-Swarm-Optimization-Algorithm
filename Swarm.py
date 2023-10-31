from Particle import Particle
import numpy as np
import math


class Swarm:
    def __init__(self, size, dim, bound_min, bound_max, v_max):
        self.size = size
        self.dim = dim
        self.population = []
        self.gbest = None
        self.gbest_value = np.inf

        for i in range(self.size):
            p = Particle(i, self.dim, bound_min, bound_max, v_max)
            self.population.append(p)

    def __str__(self):
        for i in range(self.size):
            print(self.population[i])
        return

    def upgrade_vel_swarm(self, w, c1, c2, g_best):
        for i in range(self.size):
            self.population[i].upgrade_vel(w, c1, c2, g_best)
        return

    def upgrade_position_swarm(self):
        for i in range(self.size):
            self.population[i].upgrade_position()
        return

    def upgrade_gbest(self):
        for i in range(self.size):
            if self.population[i].fitness_value_p_best < self.gbest_value:
                self.gbest_value = self.population[i].fitness_value_p_best
                self.gbest = self.population[i].x
        return

    def upgrade_pbest_swarm(self):
        for i in range(self.size):
            self.population[i].upgrade_pbest()
        return

    def evaluate_fitness_swarm(self):
        for i in range(self.size):
            self.population[i].fitness_function()
        return
