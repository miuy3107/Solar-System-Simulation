# test_acceleration.py

import pytest
class MockVector:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
    def __add__(self, other): return MockVector(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other): return MockVector(self.x - other.x, self.y - other.y, self.z - other.z)
    def __mul__(self, other): return MockVector(self.x * other, self.y * other, self.z * other)
    def __truediv__(self, other): return MockVector(self.x / other, self.y / other, self.z / other)
    def __neg__(self): return MockVector(-self.x, -self.y, -self.z)
    def __eq__(self, other): return self.x == other.x and self.y == other.y and self.z == other.z
    def __repr__(self): return f"vector({self.x}, {self.y}, {self.z})"

def vector(x, y, z): return MockVector(x, y, z)
def mag(v): return (v.x**2 + v.y**2 + v.z**2)**0.5

# ===== Hàm cần test =====
def compute_acceleration(p, bodies, G):
    total_acc = vector(0, 0, 0)
    for other in bodies:
        if p is other:
            continue
        r_vec = p.position - other.position
        dist = mag(r_vec)
        if dist < 1e-5:
            continue
        total_acc += -G * other.mass * r_vec / dist**3
    return total_acc


# ===== Mock object =====
class Body:
    def __init__(self, position, mass):
        self.position = position
        self.mass = mass


# ===== TESTS =====

def test_single_body_no_acceleration():
    p = Body(vector(0, 0, 0), 10)
    bodies = [p]
    acc = compute_acceleration(p, bodies, G=1)
    assert acc == vector(0, 0, 0)


def test_two_body_direction():
    p = Body(vector(0, 0, 0), 1)
    other = Body(vector(1, 0, 0), 10)
    acc = compute_acceleration(p, [p, other], G=1)

    assert acc.x > 0
    assert acc.y == 0
    assert acc.z == 0


def test_two_body_magnitude():
    p = Body(vector(0, 0, 0), 1)
    other = Body(vector(1, 0, 0), 10)
    acc = compute_acceleration(p, [p, other], G=2)

    expected = 20  # 2 * 10 / 1^2
    assert pytest.approx(acc.x, rel=1e-6) == expected


def test_zero_distance():
    p = Body(vector(0, 0, 0), 1)
    other = Body(vector(0, 0, 0), 10)

    acc = compute_acceleration(p, [p, other], G=1)
    assert acc == vector(0, 0, 0)


def test_multiple_bodies():
    p = Body(vector(0, 0, 0), 1)
    b1 = Body(vector(1, 0, 0), 10)
    b2 = Body(vector(0, 1, 0), 10)

    acc = compute_acceleration(p, [p, b1, b2], G=1)

    assert acc.x > 0
    assert acc.y > 0
    