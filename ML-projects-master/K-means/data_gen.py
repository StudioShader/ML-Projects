import random
import math

class data_gen:
    def __init__(self, center, N, K):
        self.center = center
        self.mass = []
        self.edges = []
        self.N = N
        self.K = K
        self.INF = 10000000000000000000000000

    def dist(self, a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def normal_gen(self):
        self.mass.clear()
        for i in range(0, self.N):
            num = random.randrange(0, 200)
            if num <= 20:
                #noise
                self.mass.append([random.randrange(30, 800), random.randrange(150, 500)])
            else:
                self.mass.append([self.center[num % 2][0] + random.randrange(-100, 120), self.center[num % 2][1] + random.randrange(-100, 100)])
        random.shuffle(self.mass)
        return self.mass

    def get_random_data(self):
        self.mass.clear()
        for i in range(0, self.N):
            num = random.randrange(0, 100)
            if num <= 7:
                self.mass.append([random.randrange(1, 1000), random.randrange(1, 600)])
            elif num <= 54:
                self.mass.append([random.randrange(100, 200), random.randrange(150, 300)])
            else:
                self.mass.append([random.randrange(750, 990), random.randrange(350, 600)])
        random.shuffle(self.mass)
        return self.mass

    def get_real_random_data(self):
        self.mass.clear()
        for i in range(0, self.N):
            self.mass.append([random.randrange(1, 1000), random.randrange(1, 600)])
        random.shuffle(self.mass)
        return self.mass

    def strip_data(self):
        self.mass.clear()
        while len(self.mass) <= self.N:
            for i in range(0, 4*self.K):
                for i in range(0, 100):
                    self.mass.append([self.center[0][0] + random.randrange(-95, 110), self.center[0][1] + random.randrange(-100, 90)])
                self.center[0][0] += 70
                self.center[0][1] += 20
        random.shuffle(self.mass)
        return self.mass

    def nested_data(self):
        self.mass.clear()
        while len(self.mass) <= self.N:
            for i in range(50, 300, 10):
                self.mass.append([i, self.center[0][1] + 100 + random.randrange(-23, 23)])
            for i in range(50, 300, 10):
                self.mass.append([i, self.center[0][1] - 100 + random.randrange(-23, 23)])
            for i in range(25, 200, 10):
                self.mass.append([self.center[0][0] + 100 + random.randrange(30, 50), i])
            for i in range(25, 200, 10):
                self.mass.append([self.center[0][0] - 100 + random.randrange(30, 50), i])
            for i in range(0, 300, 10):
                self.mass.append([self.center[0][0] + random.randrange(-15, 80), self.center[0][1] + random.randrange(-40, 50)])
        random.shuffle(self.mass)
        return self.mass

    def get_edges(self):
        for i in range(0, self.N - 1):
            for j in range(i + 1, self.N):
                self.edges.append([self.dist(self.mass[i], self.mass[j]), i, j])
        self.edges.sort()
        return self.edges