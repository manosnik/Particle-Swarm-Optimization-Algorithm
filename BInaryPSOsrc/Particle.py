import numpy as np
from bitstring import BitArray
import random
import math


class Particle:

    def __init__(self, id, ff_code, bound_min, bound_max, number_of_decimals):
        # bound_min ,bound_max coulb be determined inside Particle but if it's done in  Swarm it's faster

        self.id = id
        self.ff_code = ff_code
        self.bound_min = bound_min
        self.bound_max = bound_max
        self.number_of_decimals = number_of_decimals

        self.fitness_value = None
        self.fitness_value_p_best = np.inf

        self.bit_dim = 0
        self.compute_bit_dim()

        self.x = self.generate_random_bitstring()  # x is BitArray
        # print(f"first random pos {self.x.bin}")

        self.test_bitstring_in_bounds()

        self.p_best = self.x  # p_best is BitArray

    def __str__(self):
        return f"id:{self.id}\tx:{self.x.bin}\tfloat_pos:{self.float_position}\t fitness_value:{self.fitness_value}" \
               f"\tpbest:{self.p_best.bin}\t fitness_value_p_best:{self.fitness_value_p_best}"

    def compute_bit_dim(self):
        if self.ff_code == 1:  # Eggholder
            self.real_dim = 2
        elif self.ff_code == 2:  # Burkin 6
            self.real_dim = 2

        for i in range(self.real_dim):
            float_space = self.bound_max[i] - self.bound_min[i]
            self.bit_dim += math.floor(math.log2(float_space * math.pow(10, self.number_of_decimals))) + 1

        return

    def generate_random_bitstring(self):
        key1 = ""
        for i in range(self.bit_dim):
            temp = str(random.randint(0, 1))
            key1 += temp
        # print(key1)
        return BitArray(bin=key1)

        # tests if the position bitstring corresponds to a valid float position for the selected fitness function
        # if not it changes the position bitstring to the limits of valid space
        # In addition computes and saves the float position of the current position bitstring

    def test_bitstring_in_bounds(self):  # should be checked if self would be better to leave from some variables

        self.float_position = self.driver_bin_to_float(self.x)
        # print(self.float_position)
        flag = 0
        for i in range(self.real_dim):
            if self.float_position[i] > self.bound_max[i]:
                self.float_position[i] = self.bound_max[i]
                flag = 1
            elif self.float_position[i] < self.bound_min[i]:
                self.float_position[i] = self.bound_min[i]
                flag = 1
        if flag == 1:
            # print("out of bounds flag activated")
            self.x = self.driver_float_to_bin(self.float_position)
            # print(self.driver_bin_to_float(self.x))
        return

    def driver_bin_to_float(self, input_bitstring):
        output_float_array = np.zeros(len(self.bound_min))
        string_counter = 0
        for i in range(len(self.bound_min)):
            float_space = self.bound_max[i] - self.bound_min[i]
            number_of_bits_needed = math.floor(math.log2(float_space * math.pow(10, self.number_of_decimals))) + 1
            output = input_bitstring.bin[string_counter:string_counter + number_of_bits_needed]
            string_counter += number_of_bits_needed
            # print(output_float_array[i])
            # print(number_of_bits_needed)
            # print(output)
            output = int(output, base=2)

            # print("uint")
            # print(output_float_array[i])
            output = output / math.pow(10, self.number_of_decimals)
            output = output + self.bound_min[i]
            output_float_array[i] = output
            # print(output_float_array)
        return output_float_array

    def driver_float_to_bin(self, float_number_array):
        output_bitstring = BitArray()
        for i in range(len(float_number_array)):
            float_space = self.bound_max[i] - self.bound_min[i]
            float_number = float_number_array[i] - self.bound_min[i]
            number_of_bits_needed = math.floor(math.log2(float_space * math.pow(10, self.number_of_decimals))) + 1
            float_number = int(float_number * math.pow(10, self.number_of_decimals))
            output_bitstring.append(BitArray(uint=float_number, length=number_of_bits_needed))
        # print(f"dimensions of hybercube = {output_bitstring.len}")
        # print(output_bitstring)
        return output_bitstring

    def upgrade_vel(self, g_best):
        self.v = ((self.x ^ g_best) & self.generate_random_bitstring()) | (
                (self.x ^ self.p_best) & self.generate_random_bitstring())
        return

    def upgrade_position(self):
        self.x = self.x ^ self.v
        self.test_bitstring_in_bounds()
        return

    def upgrade_pbest(self):

        if (self.fitness_value < self.fitness_value_p_best):
            self.p_best = self.x
            self.fitness_value_p_best = self.fitness_value
        return

    def fitness_function(self):
        if self.ff_code == 1:  #Eggholder
            a = math.sqrt(math.fabs(self.float_position[1] + self.float_position[0] / 2 + 47))
            b = math.sqrt(math.fabs(self.float_position[0] - (self.float_position[1] + 47)))
            self.fitness_value = -(self.float_position[1] + 47) * math.sin(a) - self.float_position[0] * math.sin(b)

        elif self.ff_code == 2:  # Bukin N.6
            term1 = 100 * math.sqrt(abs(self.float_position[1] - 0.01 * self.float_position[0] ** 2))
            term2 = 0.01 * abs(self.float_position[0] + 10)
            self.fitness_value = term1 + term2

        return


###TEST CODE
#
#
# bound_min = [-512] * 2
# bound_max = [512] * 2
#
# p = Particle(0, 1, bound_min, bound_max, 3)
#
# # print(p.float_position)
# for i in range(100):
#     p.fitness_function()
#     p.upgrade_pbest()
#     print(p)
#     p.upgrade_vel(p.generate_random_bitstring())
#     p.upgrade_position()
#     i+=1
