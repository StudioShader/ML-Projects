import math
import random
import copy

class k_means:
    def __init__(self, mass, K):
        self.mass = mass
        self.K = K  #clusters amount
        self.N = len(mass)  #data size
        self.INF = 10000000000000000000000000
        self.centroids = []
        self.clusters = {}
        self.pref_centroids = []
        self.dx_dist = [0]*self.N

    def dist(self, a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    # - - - - - - - k-means++ - - - - - - - 
    # optimal initialization

    def initialization(self):
        self.centroids.append(copy.deepcopy(self.mass[random.randrange(1, self.N)]))

        for i in range(1, self.K):
            sum_dx = 0
            for i in range(0, self.N):
                tmp = self.INF
                for j in self.centroids:
                    tmp = min(tmp, self.dist(j, self.mass[i]))
                self.dx_dist[i] = copy.copy(tmp)
                sum_dx += tmp

            Rnd = random.random()*sum_dx

            s = 0
            for i in range(0, self.N):
                s += self.dx_dist[i]
                if s > Rnd:
                    self.centroids.append(copy.deepcopy(self.mass[i]))
                    break
    # algorithm

    def _k_means(self):    
        self.initialization()

        while self.pref_centroids != self.centroids:
            self.clusters.clear()
            self.pref_centroids = copy.deepcopy(self.centroids)

            for i in range(0, self.K):
                self.clusters[i] = []

            index = -1
            for i in self.mass:
                tmp = self.INF
                for j in range(0, self.K):
                    if self.dist(i, self.centroids[j]) < tmp:
                        index = copy.copy(j)
                        tmp = self.dist(i, self.centroids[j])

                self.clusters[index].append(copy.copy(i))

            # re-calculate centroids

            for k in range(0, self.K):
                tx_sum = 0
                ty_sum = 0
                for i in self.clusters[k]:
                    tx_sum += i[0]
                    ty_sum += i[1]

                self.centroids[k] = [ round(tx_sum / len(self.clusters[k])), round(ty_sum / len(self.clusters[k])) ]

        return self.clusters