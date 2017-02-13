from vector import Vector, EPS

from decimal import Decimal, getcontext

getcontext().prec = 30


class Plane(object):
    """Present a Plane in 3D by 'A*X+B*Y+C*Z=K', while Vector([A, B, C]) is the plane's normal vector"""

    def __init__(self, normal_vector=None, constant=None):
        self.dimension = 3
        self.normal_vector = normal_vector if normal_vector else Vector([0, 0, 0])
        assert self.normal_vector.dimension == 3  # this plane class just for 3D
        self.constant = Decimal(constant) if constant is not None else Decimal(0)

        # set base point
        A, B, C = self.normal_vector.coordinates
        if abs(A) > EPS:
            self.base_point = Vector([self.constant / A, 0, 0])
        elif abs(B) > EPS:
            self.base_point = Vector([0, self.constant / B, 0])
        elif abs(C) > EPS:
            self.base_point = Vector([0, 0, self.constant / C])
        else:
            self.base_point = None

    def __str__(self):
        A, B, C, K = self.normal_vector.coordinates + (self.constant,)
        res = ''
        if abs(A) > EPS:
            res += '{}*X'.format(A)
        if B > EPS:
            if res != '': res += ' + '
            res += '{}*Y'.format(B)
        elif B < -EPS:
            if res != '':
                res += ' - ' + '{}*Y'.format(-B)
            else:
                res += '{}*Y'.format(B)
        if C > EPS:
            if res != '': res += ' + '
            res += '{}*Z'.format(C)
        elif C < -EPS:
            if res != '':
                res += ' - ' + '{}*Z'.format(-C)
            else:
                res += '{}*Z'.format(C)
        if res == '': res = '0'
        res += ' = {}'.format(K)
        return res

    def __eq__(self, other):
        if self.normal_vector.is_zero() and other.normal_vector.is_zero(): return True
        if self.normal_vector.is_zero() or other.normal_vector.is_zero(): return False
        if not self.is_parallel_with(other): return False
        return self.base_point == other.base_point

    def is_parallel_with(self, other):
        assert not (self.normal_vector.is_zero() or other.normal_vector.is_zero())
        return self.normal_vector.is_parallel_with(other.normal_vector)

    def is_equal_with(self, other):
        return self == other


def test():
    plane1 = Plane(Vector([1, 0, -1]), 0)
    assert plane1 == plane1 and plane1.is_parallel_with(plane1) and plane1.is_equal_with(plane1)

    plane_a = Plane(Vector([-0.412, 3.806, 0.728]), -3.46)
    plane_b = Plane(Vector([1.03, -9.515, -1.82]), 8.65)
    assert plane_a == plane_b

    plane_c = Plane(Vector([2.611, 5.528, 0.283]), 4.6)
    plane_d = Plane(Vector([7.715, 8.306, 5.342]), 3.76)
    assert not plane_c.is_parallel_with(plane_d)

    plane_e = Plane(Vector([-7.926, 8.625, -7.212]), -7.95)
    plane_f = Plane(Vector([-2.642, 2.875, -2.404]), -2.443)
    assert plane_e != plane_f and plane_e.is_parallel_with(plane_f)

    return 'test passed!'


if __name__ == '__main__':
    print test()
