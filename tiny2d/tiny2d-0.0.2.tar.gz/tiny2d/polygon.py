import tiny2d as t2d


class Polygon(object):
    def __init__(self, vertices=[]):
        self.vertices = [t2d.Vector2D(*v) for v in vertices]


    def add_vertex(self, point):
        self.vertices.append(t2d.Vector2D(*point))

    def translate(self, t_vector):
        new_vertices = [p + t2d.Vector2D(*t_vector) for p in self.vertices]
        return Polygon(new_vertices)

    def contains(self, point):
        """Determine if a point is inside a given polygon or not
        Uses the 'Ray Casting' algorithm
        http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html
        """

        n = len(self.vertices)
        inside = False
        x, y = point
        p1x, p1y = self.vertices[0]
        for i in range(n + 1):
            p2x, p2y = self.vertices[i % n]
            if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
                if p1y != p2y:
                    c = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if p1x == p2x or x <= c:
                    inside = not inside
            p1x, p1y = p2x, p2y

        return inside
