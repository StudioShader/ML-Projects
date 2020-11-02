from data_gen import*
from data_drawer import*
from MST import*
from k_means import*
from convex_hull import*

N = 10000 # points quantity
sample_N = 100 # points for testing data
K = 2 # clusters amount

mass = []
edges = []
mst = []
center = [[130, 125], [700, 300]] # test centers of generated clusters

gen = data_gen(center, N, K) # data generator
dr = data_drawer(K)
ch = convex_hull()
m = MST(100, K)
#mass = gen.normal_gen()
#mass = gen.nested_data()
mass = gen.get_random_data() # all points
#mass = gen.get_real_random_data()
#mass = gen.strip_data()
sample = mass[ : sample_N]
smpl = data_gen(center, sample_N, K)
smpl.mass = sample
s_edges = smpl.get_edges()
s_edges.sort()
mst = m.get_MST(s_edges)
km_obj = k_means(mass, K)
#mass = gen.strip_data()
#convex = ch.convex_hull(result[0])
#dr.draw_MST(mst, mass)
#dr.draw_data(mass)

sample_clusters = m.get_clusters(sample) # get clusters from hierarchical clustering
centroids = m.get_centroids() # get center of clusters
res = 0

# nesting check 
for k in range(K):
    convex = ch.convex_hull(sample_clusters[k])
    for i in centroids:
        if len(convex) != 0:
            if ch.is_inside(i, convex):
                res += 1
if res <= K: # data is not nested we use k-means algorithm
    print("k-means")
    result = km_obj._k_means()
    dr.draw_clusters(result)
    for k in range(K):
        convex = ch.convex_hull(result[k])
        dr.draw_convex(convex)
else: # data is nested we use hierarchical algorithm
    print("tree")
    dr.draw_clusters(sample_clusters)
    for k in range(K):
        convex = ch.convex_hull(sample_clusters[k])
        dr.draw_convex(convex)

# retraining on new data (50% of past data is saved for training)
timed_data = [mass[:5000]]
dataset = []
for i in range(5):
    dataset.clear()
    lth = len(timed_data)
    dataset.extend(mass[5001 + (i*1000): 5000 + (i + 1)*1000])
    for i in range(lth):
        dataset.extend(copy.deepcopy(timed_data[lth - i - 1][len(timed_data[lth - i - 1])//(2**(i + 1)) : len(timed_data[lth - i - 1])]))
        dataset.sort()
        km_obj.__init__(dataset, K)
        result = km_obj._k_means()
        dr.draw_clusters(result)
        for k in range(K):
            convex = ch.convex_hull(result[k])
            dr.draw_convex(convex)
    timed_data.append(mass[5001 + (i*1000): 5000 + (i + 1)*1000])
