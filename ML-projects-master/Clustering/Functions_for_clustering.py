import copy
import Data
import numpy as np


def Points_In_Groups(points,k):
    for j in range(k):
        A = list()
        for i in range(len(points)):
            if points[i][2]==j:
                A.append( [points[i][0], points[i][1]] )
        if len(A)>2:
            Conv_A = list()
            S = Data.grahamscan(A)
            Conv_A = Data.convex_hull(S,A)
            Data.draw_shell(Conv_A)


def clast(points,centers):
    for i in range(len(points)):
        min=1000000000
        for j in range(len(centers)):
            if min > Data.metrics(points[i],centers[j]):
                min = Data.metrics(points[i],centers[j])
                points[i][2]=j
    #    group=points[i][2]
    #    draw_lines(points[i][0],points[i][1],centers[group][0],centers[group][1],False)
    Points_In_Groups(points,len(centers))
    return points


def generation_new_centers_for_kmeans(points,centers,k):
    for j in range(k):
        SumX=0
        SumY=0
        Q=0
        for i in range(len(points)):
            if points[i][2] == j:
                SumX+=points[i][0]
                Q+=1
                SumY += points[i][1]
        if Q == 0:
            continue
        else:
            centers[j][0] = SumX // Q
            centers[j][1] = SumY // Q
    return centers


def kmeans(points,centers,k):
    Data.draw_points(points, False)
    Data.draw_points(centers, True)
    points = clast(points, centers)
    Data.draw_points(points, False)

    while True:
        Data.event()
        old = copy.deepcopy(centers)
        centers = generation_new_centers_for_kmeans(points, centers,k)
        #print(centers)
        Data.draw_points(centers, True)
        points = clast(points, centers)
        Data.draw_points(points, False)
        if old == centers:
            break
    return centers, points


def array_for_hierarchical(array_of_data):
    new_array_of_data=list()
    for i in range(len(array_of_data)):
        new_array_of_data.append([[array_of_data[i][0],array_of_data[i][1]]])
    return new_array_of_data


def array_for_kmeans(array_of_data):
    new_array_of_data=list()
    for i in range(len(array_of_data)):
        for j in range(len(array_of_data[i])):
            row=array_of_data[i][j]
            row.append(i)
            new_array_of_data+=[row]
    return new_array_of_data


def generation_centers_for_hierarchical(A):
    SumX = 0
    SumY = 0
    for i in range(len(A)):
        SumX+=A[i][0]
        SumY +=A[i][1]
    return [SumX // len(A) , SumY // len(A)]


def delete_noises(array_of_data, L):
    i = 0
    min_group = L / (4*np.log(L))
    while i < len(array_of_data):
        if len(array_of_data[i]) < min_group:
            del array_of_data[i]
        else:
            i += 1
    return array_of_data


def hierarchical(points,Size):
    Data.draw_points(points, False)
    array_of_data = array_for_hierarchical(points)
    min = 0
    max_distance = Size // 15
    while min < max_distance and len(array_of_data)>1:
        Data.event()

        min=4*Size
        for i1 in range(len(array_of_data)):
            for i2 in range(len(array_of_data)):
                for j1 in range(len(array_of_data[i1])):
                    for j2 in range(len(array_of_data[i2])):
                         if Data.metrics(array_of_data[i1][j1],array_of_data[i2][j2]) <= min and array_of_data[i1][j1]!=array_of_data[i2][j2] and i1!=i2:
                             min=Data.metrics(array_of_data[i1][j1],array_of_data[i2][j2])
                             Index1=i1
                             Index2=i2
                             J1=j1
                             J2=j2

        if min < max_distance:
            Data.draw_lines(array_of_data[Index1][J1],array_of_data[Index2][J2],False)
            temp=list()
            for i in range(len(array_of_data)):
                if array_of_data[i] != array_of_data[Index1] and array_of_data[i] != array_of_data[Index2]:
                    temp.append(array_of_data[i])
            temp.append(array_of_data[Index1]+array_of_data[Index2])
            array_of_data = copy.deepcopy(temp)
            #if len(array_of_data) % 20 == 0:
             #   print("количество кластеров в иерархии:", len(array_of_data))

    array_of_data=delete_noises(array_of_data,  len(points))
    points = array_for_kmeans(array_of_data)
    Data.draw_points(points, False)

    centers=list()
    for i in range(len(array_of_data)):
         centers.append(generation_centers_for_hierarchical(array_of_data[i]))
    Data.draw_points(centers, True)

    return centers, array_of_data


def inPolygon(x, y, array):
    c = 0
    for i in range(len(array)):
        if (((array[i][1] <= y < array[i - 1][1]) or (array[i - 1][1] <= y < array[i][1])) and
                (x > (array[i - 1][0] - array[i][0]) * (y - array[i][1]) / (array[i - 1][1] - array[i][1]) + array[i][0])):
            c = 1 - c
    return c


def is_data_nested(centers, array):
    Nested = False
    for i in range(len(centers)):
        for j in range(len(array)):
            if i != j:
                u = inPolygon(centers[i][0], centers[i][1], array[j])
                if u == 1:
                    Nested = True
                    return Nested
    return Nested