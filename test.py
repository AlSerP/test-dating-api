from math import sin, cos, acos, asin, pi, sqrt 

def deg_to_rad(x):
    return x * pi / 180

def calc(long1, lat1, long2, lat2):
    print(long1, lat1)
    print(long2, lat2)
    long1 = deg_to_rad(long1)
    long2 = deg_to_rad(long2)
    lat1 = deg_to_rad(lat1)
    lat2 = deg_to_rad(lat2)
    R = 6371  # Earth radius
    d_long = long1 - long2
    # c_angle = acos(sin(self.lat) * sin(user.lat) + cos(self.lat) * cos(user.lat) * cos(d_long))
    c_angle = acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(d_long))
    
    print(c_angle)

    d_X = cos(lat2) * cos(long2) - cos(lat1) * cos(long1)
    d_Y = cos(lat2) * sin(long2) - cos(lat1) * sin(long1)
    d_Z = sin(lat2) - sin(lat1)
    C = sqrt(d_X**2 + d_Y**2 + d_Z**2)
    c_angle2 = 2 * asin(C/2)

    print(c_angle, c_angle2)

    rad_angle = c_angle * pi / 180
    print(rad_angle)
    return c_angle * R

print(calc(37.617698, 55.755864, 30.315644, 59.938955))