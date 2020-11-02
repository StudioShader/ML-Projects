class convex_hull:
    def __init__(self):
        pass

    #counter-clockwise turn
    def turn(self, a, b, c):
        return (b[0] - a[0])*(c[1] - a[1]) - (b[1] - a[1])*(c[0] - a[0])

    #build the convex hull (Graham algorithm)
    def convex_hull(self, mass):
        lower = []
        upper = []
        mass = sorted(mass)
        for p in mass:
            while len(lower) >= 2 and self.turn(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)

        for p in reversed(mass):
            while len(upper) >= 2 and self.turn(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)

        return lower[:-1] + upper[:-1]

    #return 1 if ray from C intersect AB
    def is_crossed(self, a, b, c):
        if a[1] < c[1] and b[1] > c[1] and self.turn(a, b, c) <= 0:
            return 1
        if b[1] < c[1] and a[1] > c[1] and self.turn(b, a, c) <= 0:
            return 1
        return 0

    #return true if a point inside the convex
    def is_inside(self, cent_p, conv):
        cnt = 0
        cnt += self.is_crossed(conv[0], conv[len(conv) - 1], cent_p)
        for i in range(0, len(conv) - 1):
            cnt += self.is_crossed(conv[i], conv[i + 1], cent_p)
        return cnt % 2
