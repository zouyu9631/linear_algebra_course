from vector import Vector, EPS

from decimal import Decimal, getcontext

getcontext().prec = 30

PREC = 3


class Line(object):
    """Present a line in 2D by 'A*X+B*Y=C', while Vector([A, B]) is the line's normal vector"""

    def __init__(self, normal_vector=None, constant=None):
        self.dimension = 2
        self.normal_vector = normal_vector if normal_vector else Vector([0, 0])
        assert self.normal_vector.dimension == 2  # this line class just for 2D
        self.constant = Decimal(constant) if constant is not None else Decimal(0)

        # set base point
        A, B = self.normal_vector.coordinates
        if abs(A) > EPS:
            self.base_point = Vector([self.constant / A, 0])
        elif abs(B) > EPS:
            self.base_point = Vector([0, self.constant / B])
        else:
            self.base_point = None

    def __str__(self):
        A, B, C = self.normal_vector.coordinates + (self.constant,)
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
        if res == '': res = '0'
        res += ' = {}'.format(C)
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

    def intersection_with(self, other):
        if self.is_parallel_with(other):
            if self == other:
                return self
            else:
                return None

        A, B, K1 = self.normal_vector.coordinates + (self.constant,)
        C, D, K2 = other.normal_vector.coordinates + (other.constant,)
        det = A * D - B * C
        return Vector([(D * K1 - B * K2) / det, (A * K2 - C * K1) / det])


def test():
    line1 = Line()
    line2 = Line(Vector([2, 3]), 6)
    line3 = Line(Vector([1, 0]), 1)

    # assert line1.is_parallel_with(line2)
    assert not line2.is_parallel_with(line3)
    assert line2.is_parallel_with(Line(Vector([-8, -12])))

    assert line1 == line1 and line3 != line2 and line2 == line2 and line3 == Line(Vector([2, 0]), 2)
    assert Line(Vector([0, -1.5]), 3) == Line(Vector([0, -4.5]), 9)

    assert Line(Vector([4.046, 2.836]), 1.21).intersection_with(
        Line(Vector([10.115, 7.09]), 3.025)) == Line(Vector([10.115, 7.09]), 3.025)
    assert Line(Vector([7.204, 3.182]), 8.68).intersection_with(Line(Vector([8.172, 4.114]), 9.883)) == Vector(
        [1.1727766354646, 0.0726955116633])
    assert Line(Vector([1.182, 5.562]), 6.744).intersection_with(
        Line(Vector([1.773, 8.343]), 9.525)) == None

    return 'test passed!'


if __name__ == '__main__':
    print test()
