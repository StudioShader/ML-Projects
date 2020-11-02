import copy

class MST:
    def __init__(self, N, K):
        self.N = N # vertex quantity
        self.K = K # clusters amount
        self.dad = [] # dsu
        self.rnk = [] # rank heuristic
        self.mass = []
        self.graph = []
        self.queue = []
        self.centroids = []
        for i in range(self.N):
            self.graph.append([])
        self.used = [0]*N
        self.clusters = {}
        for i in range(0, N):
            self.dad.append(i)
        for i in range(0, N):
            self.rnk.append(0)

    # - - - - - - - MST - - - - - - - 

    def get(self, u):
        if self.dad[u] == u: return u
        else:
            self.dad[u] = copy.copy(self.get(self.dad[u]))
            return self.dad[u]

    def set_union(self, a, b):
        a = copy.copy(self.get(a))
        b = copy.copy(self.get(b))
        if(self.rnk[a] < self.rnk[b]): self.dad[a] = copy.copy(b)
        if(self.rnk[b] < self.rnk[a]): self.dad[b] = copy.copy(a)
        if(self.rnk[a] == self.rnk[b]): 
            self.rnk[a]+=1
            self.dad[a] = copy.copy(b)

    def bfs(self, t):
        while len(self.queue) > 0:
            current_v = self.queue.pop(0)
            self.used[current_v] = t
            for u in self.graph[current_v]:
                if self.used[u] == 0:
                    self.queue.append(u)

    def get_MST(self, edges):
        cnt = 0
        for i in range(0, len(edges)):
            if self.get(edges[i][1]) != self.get(edges[i][2]):
                if cnt <= (self.N - self.K - 1):
                    self.set_union(edges[i][1], edges[i][2])
                    self.graph[edges[i][1]].append(copy.deepcopy(edges[i][2]))
                    self.graph[edges[i][2]].append(copy.deepcopy(edges[i][1]))
                    self.mass.append(copy.deepcopy(edges[i]))
                    cnt += 1
        return self.mass

    #---------Clusters and centroids count--------
    
    def get_clusters(self, points):
        clus = 1
        for i in range(0 ,self.K):
            self.clusters[i] = []
        for i in range(0, self.N):
            if self.used[i] == 0:
                self.queue.clear()
                self.queue.append(i)
                self.bfs(clus)
                for i in range(self.N):
                    if self.used[i] == clus:
                        self.clusters[clus - 1].append(copy.deepcopy(points[i]))
                clus += 1
        return self.clusters

    def get_centroids(self):
        for k in range(0, self.K):
            tx_sum = 0
            ty_sum = 0
            for i in self.clusters[k]:
                tx_sum += i[0]
                ty_sum += i[1]

            self.centroids.append([ round(tx_sum / len(self.clusters[k])), round(ty_sum / len(self.clusters[k])) ])
        return self.centroids
