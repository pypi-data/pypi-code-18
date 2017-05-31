from math import radians, sin, cos
from tessellation_station.command_line import CLI, Error
from decimal import Decimal, getcontext, ROUND_UP

C = CLI()
# Setup context for Deciaml
getcontext().prec = 2
getcontext().rounding = ROUND_UP

def to_actual(point, origin):
    """
    Get the actual coordinates of a point defined relative to another
    """
    actual_point = ()
    if len(point) != len(origin):
        raise ValueError

    for i, axis in enumerate(point):
        actual_point += (axis + origin[i]),
    return actual_point

@C.add_transformation
def rot(arguments):
    """
    Rotates a point around another.
    """
    rotated = []
    polygon = arguments["polygon"]
    origin = arguments["origin"]
    degree = arguments[0]
    degree_rad = radians(degree)# Math library likes radians
    about = to_actual(arguments[1], origin)
    # Save Sin and Cos of degree so we don't have to find it twice
    degree_sin = Decimal(sin(degree_rad))
    degree_cos = Decimal(cos(degree_rad))
    for point in polygon:
        point_x, point_y = (point[0]-about[0], point[1]-about[1]) # Move point so we can rotate around origin
        # Shortcuts
        if degree == 90:
            final_point =(-point_y, point_x)

        elif degree == 180:
            final_point = (-point_x, -point_y)

        elif degree == 270:
            final_point = (point_y, -point_x)
        # The real deal
        else:
            x_prime = Decimal((point_x*degree_cos) - (point_y*degree_sin)) # Rotate X and move back
            y_prime = Decimal((point_x*degree_sin) + (point_y*degree_cos)) # Rotate Y and move back
            #Convert to floats so it prints without Decimal()
            final_point = float(x_prime), float(y_prime)

        final_point = (final_point[0]+about[0], final_point[1]+about[1])
        rotated.append(final_point)

    return rotated

@C.add_transformation
def tra(arguments):
    """
    Translates a point along a vector
    """
    polygon = arguments["polygon"]
    vector = arguments[0]
    translated_polygon = []
    for point in polygon:
        x_prime = Decimal(point[0])+Decimal(vector[0]) # Add x from vector to x from point
        y_prime = Decimal(point[1])+Decimal(vector[1]) # Add y from vector to y from point
        translated_point = (x_prime, y_prime) # Turn into float so it display properly
        translated_polygon.append(translated_point)

    return translated_polygon

@C.add_transformation
def ref(arguments):
    """
    Reflects a polygon across a straight line on an axis.
    """
    reflected = []
    polygon = arguments["polygon"]
    origin = arguments["origin"]
    axis = arguments[0].upper()
    line = arguments[1]
    if axis not in ["X", "Y"]:
        raise(Error("{} is not an axis".format(axis)))

    for point in polygon:
        # Move so we can reflect with the real origin
        origin_point = point[0]-origin[0], point[1]-origin[1]
        # I think this works on the fact that reflected points are
        # equadistant to the line of reflection
        reflect_axis = lambda a : Decimal((line - a)+ line)
        if axis == "X":
            reflected_point = (reflect_axis(origin_point[0]), origin_point[1])

        if axis == "Y":
            reflected_point = (origin_point[0], reflect_axis(origin_point[1]))

        reflected_point = reflected_point[0]+origin[0], reflected_point[1]+origin[1]
        reflected.append(reflected_point)

    return reflected

@C.add_transformation
def sca(arguments):
    polygon = arguments["polygon"]
    scale_factor = arguments[0]
    scaled_polygon = []
    for point in polygon:
        scaled_point = Decimal(point[0])*Decimal(scale_factor), Decimal(point[1])*Decimal(scale_factor)
        scaled_polygon.append(scaled_point)

    return scaled_polygon



@C.add_configuration
def polygon(arguments):
    C.polygon = arguments[0]

@C.add_configuration
def leave(arguments):
    polygon = arguments["polygon"]
    print("Final point: {}".format(polygon))
    print("Goodbye!")
    exit()