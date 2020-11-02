import random
import numpy as np
import pygame as pg

def generation(n,Size,centers):
    point = list()
    for i in range(n):
        x=random.randint(0,Size)
        y=random.randint(0,Size)
        if centers:
            point += [[x, y]]
        else:
            point += [[x, y, -1]]
    return point


def generation_in_groups(n,k,r,Size):
    point = list()
    noise = 0 # int( n / (7*np.log(k)) ) # шумы 
    for j in range(k):
        x0=random.randint(r, 2*Size-r)
        y0=random.randint(r, Size-r)
        i=0
        while i < (n-noise) // k:
            x = random.randint(x0-r, x0+r)
            y = random.randint(y0-r, y0+r)
            if metrics([x0,y0],[x,y]) > r:
                continue
            else:
                point += [[x, y, -1]]
                i+=1
    for i in range(noise):
        x = random.randint(0, Size*2)
        y = random.randint(0, Size)
        point += [[x, y, -1]]
    return point


def generation_in_ring(n, min_rad, max_rad, Size):
    point = list()
    l = 0
    x0 = Size
    y0 = Size // 2
    while l < n:
        x = random.randint(1, Size*2-1)
        y = random.randint(1, Size-1)
        if metrics([x0,y0],[x,y]) <= max_rad and ( metrics([x0,y0],[x,y]) <= min_rad or metrics([x0,y0],[x,y]) >= (max_rad-min_rad) ):
            point += [[x, y, -1]]
            l += 1
    return point


def metrics(a,b):
    return np.sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 )


def draw_points(a,IsItCenters):
    if IsItCenters:
        for i in range(len(a)):
            pg.draw.circle(sc, RED, (a[i][0], a[i][1]), 3)
    else:
        sc.fill(WHITE)
        for i in range(len(a)):
            pg.draw.circle(sc, BLACK, (a[i][0], a[i][1]), 2)
        pg.time.wait(MS)
    pg.display.flip()



def draw_lines(a,b,is_it_shell):
    if is_it_shell:
        pg.draw.line(sc, GREEN, a, b, 3)
    else:
        pg.draw.line(sc, LIGHT_BLUE, a, b, 2)
    pg.display.flip()



def draw_shell(A):
    for i in range(1, len(A)):
        #print(A[i - 1], A[i])
        draw_lines( [A[i-1][0], A[i-1][1]], [A[i][0], A[i][1]],True)
    draw_lines([ A[0][0], A[0][1] ], [ A[len(A)-1][0], A[len(A)-1][1] ],True)
    pg.time.wait(MS)


def rotate(A,B,C):
  return (B[0]-A[0])*(C[1]-B[1])-(B[1]-A[1])*(C[0]-B[0])


def grahamscan(A):
    n = len(A)  # число точек
    P = list(range(n))  # список номеров точек
    for i in range(1, n):
        if A[P[i]][0] < A[P[0]][0]:  # если P[i]-ая точка лежит левее P[0]-ой точки
            P[i], P[0] = P[0], P[i]  # меняем местами номера этих точек
    for i in range(2, n):  # сортировка вставкой
        j = i
        while j > 1 and (rotate(A[P[0]], A[P[j - 1]], A[P[j]]) < 0):
            P[j], P[j - 1] = P[j - 1], P[j]
            j -= 1
    S = [P[0], P[1]]  # создаем стек
    for i in range(2, n):
        while rotate(A[S[-2]], A[S[-1]], A[P[i]]) < 0:
            del S[-1]  # pop(S)
        S.append(P[i])  # push(S,P[i])
    return S


def convex_hull(S, A):
    Conv_A = list()
    for j in range(len(S)):
        Conv_A.append(A[S[j]])
    return Conv_A


def random_part_of_array(array,  k):
    random_part = list()
    for i in range(k):
        indx = random.randint(0, len(array)-1)
        random_part.append(array[indx])
    return


def event():
    pg.event.get()

def get_Size():
    return Size


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
RED = (255, 0, 0)

MS = 100
Size = 750
pg.init()
sc = pg.display.set_mode((Size*2, Size))
pg.display.flip()