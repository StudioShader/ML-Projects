import math
N = 50
r = 100 #radius
mas = []
for i in range(20):
    mas += [open('writeanswer' + str(i) + '.txt', 'w')]
for k in range(20):
    r = 10 + k * 10
    for i in range(N):
        angle = i * math.pi * 2 / N;
        mas[k].write(str(i) + " " + str(math.cos(angle) * r) + " " + str(math.sin(angle) * r))
        mas[k].write('\n')