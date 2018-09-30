# Python version used in this module: 3.5.2
import sys
import math
import random


class Place:
    """A representation of a place.

    Attributes:
        latitude (float): The latitude value in the geographic coordinate system.
        longitude (float): The longitude value in the geographic coordinate system.
        city (str): The city where the place is located.
        state (str): The state where the place is located.
    """

    def __init__(self, latitude, longitude, city, state):
        """Returns a representation of a place."""
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.state = state

    def compute_distance(self, other_place):
        """ Calculates the Haversine distance in km between the current place and other place.

        Args:
            other_place (Place): Another place

        Returns:
            float: The distance between the two places in km
        """
        radius = 6371
        dist_lat = math.radians(other_place.latitude - self.latitude)
        dist_long = math.radians(other_place.longitude - self.longitude)
        a = (math.sin(dist_lat / 2) * math.sin(dist_lat / 2) + math.cos(math.radians(
            self.latitude)) * math.cos(math.radians(other_place.latitude))
            * math.sin(dist_long / 2) * math.sin(dist_long / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return radius * c


class Truck:
    """A representation of a truck in the system.

    Attributes:
        name (str): The name of the truck.
        place (Place): The place where the truck is.
    """

    def __init__(self, name, place):
        """Returns a representation of a truck."""
        self.name = name
        self.place = place
        self.rate = random.randInt(6)


class Cargo:
    """ A representation of a cargo in the system.

    Attributes:
        product (str): The name of the product.
        orig_place (Place): The place of origin of the cargo.
        dest_place (Place): The place of destination of the cargo.
        distance (float): Distance in km between the place of origin and the place
        of destination.
    """

    def __init__(self, product, orig_place, dest_place):
        """Returns a representation of a cargo."""
        self.product = product
        self.orig_place = orig_place
        self.dest_place = dest_place
        self.distance = self.orig_place.compute_distance(self.dest_place)


class VehicleRoutingProblem:
    """A representation of a vehicle routing problem

    Attributes:
        trucks (list): The list of trucks in the system.
        cargoes (list): The list of cargoes in the system.
        truck_count (int): The number of trucks in the system.
        cargo_count (int): The number of cargoes in the system.
        __dist_matrix (list): A private matrix containing the distances between the
        trucks and the origin places of the cargoes.
    """

    class Solution:
        """A representation for a solution of the vehicle routing problem.

        Attributes:
            val (float): Total distance traveled by the trucks.
            vector (list): Configuration of which truck transports which cargo.
        """

        def __init__(self, val=0, vector=None):
            """Returns a representation of a solution."""
            self.val = val
            self.vector = vector

    def __init__(self):
        """Returns a representation of a vehicle routing problem."""
        self.trucks = []
        self.cargoes = []
        self.truck_count = 0
        self.cargo_count = 0
        self.__dist_matrix = None

    def add_truck(self, truck):
        """Adds a truck to the vehicle routing problem."""
        self.trucks.append(truck)
        self.truck_count += 1

    def add_cargo(self, cargo):
        """Adds a cargo to the vehicle routing problem."""
        self.cargoes.append(cargo)
        self.cargo_count += 1

    def clear_trucks(self):
        """Removes all trucks of the vehicle routing problem."""
        self.trucks.clear()
        self.truck_count = 0

    def clear_cargoes(self):
        """Removes all cargoes of the vehicle routing problem."""
        self.cargoes.clear()
        self.cargo_count = 0

    def solve(self):
        """Solves the vehicle routing problem.

        This method finds the optimal mapping of trucks to cargoes minimizing the
        overall distances the trucks must travel​. Each truck can only carry up to
        one cargo, each truck can only make up to one trip and that some trucks
        may not be used at all.

        Returns:
            VehicleRoutingProblem.Solution: The solution of the problem.
        """
        if self.cargo_count == 0:
            print('There are not cargoes in the system.')
            return None
        if self.truck_count == 0:
            print('There are not trucks in the system.')
            return None
        if self.cargo_count > self.truck_count:
            print('We cannot find a solution. The number of cargos {} must be less or equal than '
                  'the number of trucks {}'.format(self.cargo_count, self.truck_count))
            return None

        # Compute the distance matrix between the locations of the trucks and
        # the places of origin of the cargoes. The rows represent the trucks
        # and the columns represent the cargoes.
        self.__dist_matrix = [[0] * self.cargo_count for _ in range(self.truck_count)]
        # Compute the minimum distances to the origin locations of the cargoes
        # from the trucks. This computation is used to estimate lower bounds of
        # the partial solutions.
        min_dist_cargos = [sys.maxsize] * self.cargo_count
        for i in range(self.truck_count):
            for j in range(self.cargo_count):
                self.__dist_matrix[i][j] = self.trucks[i].place.compute_distance(
                    self.cargoes[j].orig_place)
                if self.__dist_matrix[i][j] < min_dist_cargos[j]:
                    min_dist_cargos[j] = self.__dist_matrix[i][j]

        # Compute a first feasible solution by means of a greedy approach. Each
        # cargo is carried by the remaining truck that is closer to it.
        sol = VehicleRoutingProblem.Solution(0, [-1] * self.cargo_count)

        for j in range(self.cargo_count):
            min_dist = sys.maxsize
            min_truck = -1
            for i in range(self.truck_count):
                if self.__dist_matrix[i][j] < min_dist and i not in sol.vector:
                    min_dist = self.__dist_matrix[i][j]
                    min_truck = i
            sol.vector[j] = min_truck
            sol.val += min_dist

        curr_sol = VehicleRoutingProblem.Solution(0, [-1]*self.cargo_count)
        # Solve the integer optimization problem by the branch and bound paradigm.
        # Here recursion is used but I could have used a stack or a priority queue.
        # Also I could have used another strategy to compute the first solution or
        # to compute the lower bound of the partial solutions. However, for the
        # given scenario in the task (count of trucks and count of cargoes of the
        # provided files) this implementation is good enough.
        self.__solve_rec(curr_sol, 0, sol, min_dist_cargos)

        # Add to the solution the distance traveled between the endpoints of the cargoes
        for c in self.cargoes:
            sol.val += c.distance
        self.print_solution(sol)
        return sol

    def __check_the_ranks(self, curr_sol, best_sol):
        for cargo,truck in enumerate (curr_sol.vector):
            if truck.rate > self.trucks[best_sol.vector[cargo].rate]
                return True
        return False


    def __solve_rec(self, curr_sol, curr_cargo, best_sol, min_dist_cargos):
        """ Solves the vehicle routing problem associated to the restrictions mentioned
         in the :func:'~loadsmart.VehicleRoutingProblem.solve' by a branch and bound paradigm.

        Args:
            curr_sol (Solution): The current solution.
            curr_cargo (int): The current cargo to be taken in the current solution.
            best_sol (Solution): The best solution found until now.
            min_dist_cargos (list): The minimum distances to each cargo from all trucks.
        """
        # Check if the current solution is a complete solution. If it is and it is better
        # than the best solution found until now then saves it.
        if curr_cargo == self.cargo_count:
            if curr_sol.val < best_sol.val or (curr_sol.val == best_sol.val and self.__check_the_ranks(curr_sol, best_sol)):
                best_sol.vector = curr_sol.vector[:]
                best_sol.val = curr_sol.val
            return

        # Check the lower bound value of the current partial solution. For this we use
        # the best possible distance to the cargoes.
        tmp = curr_sol.val
        for i in range(curr_cargo, self.cargo_count):
            tmp += min_dist_cargos[i]

        if tmp < best_sol.val:
            for i in range(self.truck_count):
                if i not in curr_sol.vector and self.__dist_matrix[i][curr_cargo] \
                        + curr_sol.val < best_sol.val:
                    curr_sol.vector[curr_cargo] = i
                    curr_sol.val += self.__dist_matrix[i][curr_cargo]
                    self.__solve_rec(curr_sol, curr_cargo + 1, best_sol, min_dist_cargos)
                    curr_sol.vector[curr_cargo] = -1
                    curr_sol.val -= self.__dist_matrix[i][curr_cargo]

    def print_solution(self, sol):
        """Print the solution of the vehicle routing problem.

        Args:
            sol (Solution): The solution to be printed.
        """
        print('Total distance traveled is {0:,.2f} km.'.format(sol.val))
        for i, val in enumerate(sol.vector):
            print('Cargo {0} with {1} is transported by truck {2} with name {3} traveling {4:,'
                  '.2f} km.'.format(i + 1, self.cargoes[i].product, val + 1, self.trucks[val].name,
                                   (self.__dist_matrix[val][i] if self.__dist_matrix else
                                   self.trucks[val].place.compute_dist(self.cargoes[i].orig_place))
                                   + self.cargoes[i].distance))

if __name__ == '__main__':
    vrp = VehicleRoutingProblem()
    # Read the truck file.
    with open('trucks.csv') as f:
        truck_lines = f.read().splitlines()
    for i in range(1, len(truck_lines)):
        l = truck_lines[i].split(',')
        new_truck = Truck(l[0], Place(float(l[3]), float(l[4]), l[1], l[2]))
        vrp.add_truck(new_truck)

    # Read the cargoes file.
    with open('cargo.csv') as f:
        cargo_lines = f.read().splitlines()
    for i in range(1, len(cargo_lines)):
        l = cargo_lines[i].split(',')
        new_cargo = Cargo(l[0], Place(float(l[3]), float(l[4]), l[1], l[2]), Place(float(l[7]),
                          float(l[8]), l[5], l[6]))
        vrp.add_cargo(new_cargo)

    # Solve the problem and print the solution.
    vrp.solve()
