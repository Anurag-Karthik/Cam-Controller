from math import sqrt

def distanceBetweenPoints(p1x, p1y, p2x, p2y):
    return sqrt(((p2x - p1x) * (p2x - p1x)) + ((p2y - p1y) * (p2y - p1y)))

print(distanceBetweenPoints(2, 5, 5, 9))