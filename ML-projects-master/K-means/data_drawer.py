import stddraw

class data_drawer:
    def __init__(self, K):
        stddraw.setCanvasSize(1000, 600)
        stddraw.setXscale(1, 1000)
        stddraw.setYscale(1, 600)
        stddraw.setPenColor(stddraw.BLACK)
        self.K = K #clusters amount

    def draw_data(self, mass):
        stddraw.clear()
        for i in mass:
            #print(i)
            stddraw.point(i[0], i[1])
        stddraw.show(2000)
    
    def print_data(self, mass):
        for i in mass:
            print(i)

    def draw_MST(self, MST, mass):
        stddraw.clear()
        for i in MST:
            stddraw.line(mass[i[1]][0], mass[i[1]][1], mass[i[2]][0], mass[i[2]][1])
        stddraw.show(2000)

    def draw_clusters(self, clusters):
        stddraw.clear()
        for k in range(0, self.K):
            for i in clusters[k]:
                stddraw.point(i[0], i[1])
            stddraw.show(2000)

    def print_clusters(self, clusters):
        for k in range(0, self.K):
            for i in clusters[k]:
                print(i[0], i[1])

    def draw_convex(self, convex):
        stddraw.line(convex[-1][0], convex[-1][1], convex[0][0], convex[0][1])
        for i in range(len(convex) - 1):
            stddraw.line(convex[i][0], convex[i][1], convex[i + 1][0], convex[i + 1][1])
        stddraw.show(2000)

    def draw_convex_point(self, convex):
        for i in convex:
            stddraw.point(i[0], i[1])
        stddraw.show(2000)