from Swarm import Swarm


class Pso:
    def __init__(self, size, dim, bound_min, bound_max, v_max, iterations):
        self.iterations = iterations
        self.s = Swarm(size, dim, bound_min, bound_max, v_max)

        for i in range(self.iterations):
            self.s.evaluate_fitness_swarm()
            self.s.upgrade_pbest_swarm()
            self.s.upgrade_gbest()
            self.s.upgrade_vel_swarm(w=0.9 - ((0.9 - 0.4) / self.iterations) * i, c1=2, c2=2, g_best=self.s.gbest)
            self.s.upgrade_position_swarm()
        print(f"best is {self.s.gbest_value} at {self.s.gbest}")



bound_min = [-15, -3]
bound_max = [-5, 3]
v_max = [5, 1]

algorithm = Pso(30, 2, bound_min, bound_max, v_max, 100)
