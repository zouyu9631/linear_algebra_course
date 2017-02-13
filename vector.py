from math import cos, sin, acos, asin, radians, degrees, pi

from decimal import Decimal, getcontext

getcontext().prec = 30

EPS = 1e-10


class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(Decimal(x) for x in coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        # return self.coordinates == v.coordinates # for prec .....
        assert self.dimension == v.dimension

        return all(abs(x - y) < EPS for (x, y) in zip(self.coordinates, v.coordinates))

    def __add__(self, v):
        assert self.dimension == v.dimension
        return Vector([self.coordinates[i] + v.coordinates[i] for i in range(len(self.coordinates))])

    def __sub__(self, v):
        assert self.dimension == v.dimension
        return Vector([self.coordinates[i] - v.coordinates[i] for i in range(len(self.coordinates))])

    def __mul__(self, v):
        assert isinstance(v, int) or isinstance(v, float) or isinstance(v, Decimal)
        return Vector([c * Decimal(v) for c in self.coordinates])

    def is_zero(self):
        return sum(abs(x) for x in self.coordinates) < EPS

    def magnitude(self):
        return sum(c * c for c in self.coordinates).sqrt()

    def normalized(self):
        mag = self.magnitude()
        if mag == 0: raise ValueError('This Vector is ZERO Vector, has NO Magnitude')
        return self * (1.0 / float(mag))

    def plus(self, v):
        return self + v

    def minus(self, v):
        return self - v

    def times_scalar(self, n):
        return self * n

    def dot_product(self, v):
        assert self.dimension == v.dimension
        return sum(a * b for (a, b) in zip(self.coordinates, v.coordinates))

    def angle_with(self, v, unit='R'):  # unit: R for Radians, D for Degrees
        assert self.dimension == v.dimension
        len_a = self.magnitude()
        len_b = v.magnitude()
        if len_a * len_b == 0: raise ValueError('There is a ZERO Vector')
        res = acos(self.dot_product(v) / (len_a * len_b))
        if unit == 'R':
            return res
        elif unit == 'D':
            return degrees(res)
        else:
            raise ValueError('Unit must be R(Radians) or D(Degrees)')

    def is_parallel_with(self, v):
        assert self.dimension == v.dimension
        return self.is_zero() or v.is_zero() or self.angle_with(v) in (0, pi)

    def is_orthogonal_with(self, v):
        assert self.dimension == v.dimension
        return abs(self.dot_product(v)) < EPS

    def component_project_to(self, v):
        """self_project_to_v = (self.dot_product(v.normal)) * v.normal"""
        assert self.dimension == v.dimension
        if v.is_zero(): raise ValueError('Cannot Project on a ZERO Vector')
        u = v.normalized()
        return u * (self.dot_product(u))

    def component_orthogonal_to(self, v):
        return self - self.component_project_to(v)

    def cross_product(self, v):
        assert 1 < self.dimension == v.dimension < 4  # only for 2D or 3D
        if self.dimension == 2:
            x1, y1, z1 = self.coordinates + (0,)
            x2, y2, z2 = v.coordinates + (0,)
        else:
            x1, y1, z1 = self.coordinates
            x2, y2, z2 = v.coordinates

        return Vector([y1 * z2 - y2 * z1, x2 * z1 - x1 * z2, x1 * y2 - x2 * y1])

    def area_of_parallelogram(self, v):
        return self.cross_product(v).magnitude()

    def area_of_triangle(self, v):
        return self.area_of_parallelogram(v) / Decimal(2)


def test():
    v = Vector([1, 2, 3])
    v2 = Vector(range(1, 4))
    v3 = Vector((-1, 2, -3))

    # assert str(v) == 'Vector: (1, 2, 3)'
    # assert str(v3) == 'Vector: (-1, 2, -3)'
    assert v == v2
    assert v != v3
    assert Vector([0] * 5).is_zero()

    assert v + v3 == Vector([0, 4, 0])
    assert v - v3 == Vector([2, 0, 6])
    assert v * 3 == Vector([3, 6, 9])

    assert Vector([3, 4]).magnitude() == 5
    assert Vector([0, 2]).normalized() == Vector([0, 1])

    v4 = Vector([0, 5])
    v5 = Vector([6, 0])
    assert v.dot_product(v3) == -6
    assert v4.angle_with(v5) == pi / 2
    assert v4.angle_with(v5, 'D') == 90.0

    assert is_same(Vector([7.887, 4.138]).dot_product(Vector([-8.802, 6.776])), -41.382286)
    assert is_same(Vector([-5.955, -4.904, -1.874]).dot_product(Vector([-4.496, -8.755, 7.103])), 56.397178)
    assert is_same(Vector([3.183, -7.627]).angle_with(Vector([-2.668, 5.319]), 'R'), 3.07202630984)
    assert is_same(Vector([7.35, 0.221, 5.188]).angle_with(Vector([2.751, 8.259, 3.985]), 'D'), 60.2758112052)

    v0 = Vector([0, 0, 0])
    assert v3.is_parallel_with(v3 * 2)
    assert v3.is_parallel_with(v3 * -0.89)
    assert v4.is_orthogonal_with(v5)
    assert v0.is_orthogonal_with(v0)
    assert v0.is_parallel_with(v0)
    assert v0.is_orthogonal_with(v)
    assert v.is_parallel_with(v0)

    assert Vector([-7.579, -7.88]).is_parallel_with(Vector([22.737, 23.64]))
    assert not Vector([-7.579, -7.88]).is_orthogonal_with(Vector([22.737, 23.64]))
    assert not Vector([-2.029, 9.97, 4.172]).is_parallel_with(Vector([-9.231, -6.639, -7.245]))
    assert not Vector([-2.029, 9.97, 4.172]).is_orthogonal_with(Vector([-9.231, -6.639, -7.245]))
    assert not Vector([-2.328, -7.284, -1.214]).is_parallel_with(Vector([-1.821, 1.072, -2.94]))
    assert Vector([-2.328, -7.284, -1.214]).is_orthogonal_with(Vector([-1.821, 1.072, -2.94]))

    assert v5.component_project_to(v4) == Vector([0, 0])
    assert v.component_project_to(Vector([0, 0, 1])) == Vector([0, 0, 3])
    assert v5.component_orthogonal_to(v4) == v5
    assert v.component_orthogonal_to(Vector([0, 0, 1])) == Vector([1, 2, 0])

    assert Vector([3.039, 1.879]).component_project_to(Vector([0.825, 2.036])) == Vector(
        (1.082606962484467, 2.671742758325303))
    assert Vector([-9.88, -3.264, -8.159]).component_orthogonal_to(Vector([-2.155, -9.353, -9.473])) == Vector(
        (-8.350081043195763, 3.376061254287722, -1.4337460427811841))
    assert Vector([3.009, -6.172, 3.692, -2.51]).component_project_to(
        (Vector([6.404, -9.144, 2.759, 8.718]))) == Vector(
        (1.96851616721409, -2.8107607484393564, 0.8480849633578504, 2.679813233256158))
    assert Vector([3.009, -6.172, 3.692, -2.51]).component_orthogonal_to(
        (Vector([6.404, -9.144, 2.759, 8.718]))) == Vector(
        (1.0404838327859098, -3.3612392515606433, 2.8439150366421497, -5.189813233256158))

    assert Vector([1, 0]).cross_product(Vector([0, 1])) == Vector([0, 0, 1])
    assert Vector([1, 0]).area_of_parallelogram(Vector([0, 1])) == 1

    assert Vector([8.462, 7.893, -8.187]).cross_product(Vector([6.984, -5.975, 4.778])) == Vector(
        (-11.204571, -97.609444, -105.685162))
    assert is_same(Vector([-8.987, -9.838, 5.031]).area_of_parallelogram(Vector([-4.268, -1.861, -8.866])),
                   142.1222214018)
    assert is_same(Vector([1.5, 9.547, 3.691]).area_of_triangle(Vector([-6.007, 0.124, 5.772])), 42.5649373994)

    return "test passed"


def is_same(a, b):
    return abs(Decimal(a) - Decimal(b)) < EPS


if __name__ == '__main__':
    print test()
