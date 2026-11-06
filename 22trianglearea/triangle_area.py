"""
This is script to calculate area of triangle with different methods, getting spicy at the end. 

Plan:
+ ah2 classical method 
+  Heron's formula
+ 2 sides 1 angel 
+ 1 side 2 angels, bool for opposite angel
+ grid method, using coordinates of vertices
"""
import math

PI=math.pi # this is Pi constant, used in some calculations

def area_ah2(base, height):
    """Calculate triangle area using base and height."""

    try:
        base = float(base)
        height = float(height)
    except (ValueError, TypeError):
        raise ValueError("Base and height must be numbers")

    if base <= 0 or height <= 0:
        raise ValueError("Base and height must be positive")

    return 0.5 * base * height

test1=area_ah2(10, 5)
print(test1)  # Output: 25.0

def area_heron(a, b, c):
    """Calculate triangle area using Heron's formula."""

    try:
        a = float(a)
        b = float(b)
        c = float(c)
    except (ValueError, TypeError):
        raise ValueError("Sides must be numbers")

    if a <= 0 or b <= 0 or c <= 0:
        raise ValueError("Sides must be positive")

    if a + b <= c or a + c <= b or b + c <= a:
        raise ValueError("Invalid triangle sides")

    s = (a + b + c) / 2
    area_squared = s * (s - a) * (s - b) * (s - c)

    if area_squared < 0:
        raise ValueError("Invalid triangle sides")

    return area_squared ** 0.5 # math.sqrt woudl work too

test2=area_heron(3, 4, 5)
print(test2)  # Output: 6.0

def area_two_sides_one_angle(a, b, angle_degrees, radians=False):
    """Calculate triangle area using two sides and the included angle.
    a,b are the lengths of the two sides, and angle_degrees is the included angle in degrees.
    angle_degrees must be between 0 and 180 degrees (exclusive). If radians is True, angle_degrees is treated as radians.
    """

    try:
        a = float(a)
        b = float(b)
        angle_degrees = abs(float(angle_degrees))
    except (ValueError, TypeError):
        raise ValueError("Sides and angle must be numbers")

    if a <= 0 or b <= 0:
        raise ValueError("Sides must be positive")

    angle_radians = angle_degrees if radians else math.radians(angle_degrees)

    if angle_radians <= 0 or angle_radians >= math.pi:
        raise ValueError("Angle must be between 0 and 180 degrees (exclusive)")

    return 0.5 * a * b * math.sin(angle_radians)

test3=area_two_sides_one_angle(3, 4, 70)
print(test3)  # Output: 5.641895835477563

import math

def area_one_side_two_angles(a, angle1, angle2, opposite_angle=1, radians=False):

    try:
        a = float(a)
        angle1 = float(angle1)
        angle2 = float(angle2)
    except (ValueError, TypeError):
        raise ValueError("Side and angles must be numbers")

    if a <= 0:
        raise ValueError("Side must be positive")

    if not radians:
        angle1 = math.radians(angle1)
        angle2 = math.radians(angle2)

    if not (0 < angle1 < math.pi and 0 < angle2 < math.pi):
        raise ValueError("Angles must be between 0 and 180 degrees")

    angle3 = math.pi - angle1 - angle2

    if angle3 <= 0:
        raise ValueError("Sum of angles must be less than 180 degrees")

    if opposite_angle == 1:
        A, B, C = angle1, angle2, angle3 # A is opposite, B, C are sides
    elif opposite_angle == 2:
        A, B, C = angle2, angle1, angle3
    else:
        raise ValueError("opposite_angle must be 1 or 2")

    area = (a**2 * math.sin(B) * math.sin(C)) / (2 * math.sin(A)) # opposite angle is angle A, side a is opposite angle A

    return area


test4=area_one_side_two_angles(5, PI/2, math.radians(53.13),radians=True)
print(test4)  

# this will be grid method, using coordinates of vertices
# and now i wan to accept triplet of tuples, each tuple is a vertex of triangle, and calculate area using grid method
def area_grid_method_tuples(*vertices):
    """Calculate triangle area using coordinates of vertices (grid method).
    vertices is a list of three tuples, each tuple is (x, y) coordinates of a vertex.
    """
    if len(vertices) != 3:
        raise ValueError("There must be exactly three vertices")
    if any(len(vertex) != 2 for vertex in vertices):
        raise ValueError("Each vertex must contain exactly two coordinates")

    try:
        x1, y1 = float(vertices[0][0]), float(vertices[0][1])
        x2, y2 = float(vertices[1][0]), float(vertices[1][1])
        x3, y3 = float(vertices[2][0]), float(vertices[2][1])
    except (ValueError, TypeError):
        raise ValueError("Coordinates must be numbers")

    
    return area_grid_method(x1, y1, x2, y2, x3, y3)

def area_grid_method(x1, y1, x2, y2, x3, y3):
    """Calculate triangle area using coordinates of vertices (grid method)."""
    try:
        x1, y1 = float(x1), float(y1)
        x2, y2 = float(x2), float(y2)
        x3, y3 = float(x3), float(y3)
    except (ValueError, TypeError):
        raise ValueError("Coordinates must be numbers")

    area = abs((x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)) / 2.0)
    return area

test5=area_grid_method_tuples((0, 0), (4, 0), (2, 3))
print(test5)  # Output: 6.0
