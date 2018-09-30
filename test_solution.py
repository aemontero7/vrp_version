# Python version used in this module: 3.5.2
import unittest
from loadsmart import VehicleRoutingProblem, Cargo, Truck, Place


class PlaceTestCase(unittest.TestCase):

    def test_compute_distance(self):
        p1 = Place(48.1372, 11.5756, 'Munich', None)
        p2 = Place(52.5186, 13.4083, 'Berlin', None)
        self.assertEqual(round(p1.compute_distance(p2), 1), 504.2, 'Incorrect answer after'
                                                                   'computing distance between'
                                                                   ' two places.')

        p1 = Place(36.876719, -89.5878579, 'Sikeston', 'MO')
        p2 = Place(32.9342919, -97.0780654, 'Grapevine', 'TX')
        self.assertEqual(round(p1.compute_distance(p2), 1), 811.2, 'Incorrect answer after'
                                                                   'computing distance between'
                                                                   'two places.')


class VehicleRoutingProblemTestCase(unittest.TestCase):

    def test_solve(self):
        vrp = VehicleRoutingProblem()
        self.assertIsNone(vrp.solve(), 'There cannot be a solution because there are not'
                                       'cargoes in the problem.')

        new_cargo = Cargo('Light bulbs', Place(36.876719, -89.5878579, 'Sikeston', 'MO'),
                          Place(32.9342919, -97.0780654, 'Grapevine', 'TX'))
        vrp.add_cargo(new_cargo)
        self.assertIsNone(vrp.solve(), 'There cannot be a solution because there are not'
                                       ' trucks in the problem.')

        new_truck = Truck('Hartford Plastics Incartford', Place(34.79981, -87.677251, 'Florence',
                                                                'AL'))
        vrp.add_truck(new_truck)
        sol = vrp.solve()
        self.assertEqual(round(sol.val, 1),
                         round(vrp.cargoes[0].distance + vrp.trucks[0].place.compute_distance(
                              vrp.cargoes[0].orig_place), 1), 'There is one possible solution in a '
                                                              'problem with a truck and a cargo')
        self.assertEqual(sol.vector, [0], 'The only cargo is carried by the only truck.')

        new_cargo = Cargo('Recyclables', Place(37.1298517, -80.4089389, 'Christiansburg', 'VA'),
                          Place(28.6934076, -81.5322149, 'Apopka', 'FL'))
        vrp.add_cargo(new_cargo)
        self.assertIsNone(vrp.solve(), 'There cannot be a solution. The number of cargoes is'
                                       ' greater than the number of trucks.')

        new_truck = Truck('Apples', Place(30.876719, -95.876719, 'Lenapah', 'OK'))
        vrp.add_truck(new_truck)
        sol = vrp.solve()
        self.assertEqual(round(sol.val, 1),
                         round(vrp.cargoes[0].distance + vrp.cargoes[1].distance + vrp.trucks[0].
                               place.compute_distance(vrp.cargoes[1].orig_place) + vrp.trucks[1].
                               place.compute_distance(vrp.cargoes[0].orig_place), 1),
                         'This is the traveled distance for an optimal solution different from '
                         'the greedy solution.')
        self.assertEqual(sol.vector, [1, 0], 'The optimal solution is different from the greedy '
                                             'solution.')

        new_truck = Truck('Oranges', Place(30.876719, -94.876719, 'Lenapah2', 'OK'))
        vrp.add_truck(new_truck)
        sol = vrp.solve()
        self.assertEqual(round(sol.val, 1),
                         round(vrp.cargoes[0].distance + vrp.cargoes[1].distance + vrp.trucks[0].
                               place.compute_distance(vrp.cargoes[1].orig_place) + vrp.trucks[2].
                               place.compute_distance(vrp.cargoes[0].orig_place), 1),
                         'This is the traveled distance for an optimal solution different from '
                         'the greedy solution.')
        self.assertEqual(sol.vector, [2, 0], 'The optimal solution is different from the greedy '
                                             'solution.')


if __name__ == '__main__':
    unittest.main()

