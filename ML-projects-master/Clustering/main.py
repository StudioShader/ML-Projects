from sklearn.utils import shuffle
import Data
import Functions_for_clustering as Fc
import pygame as pg


k = 8 #int(input()) # количество групп точек
n = 4000 #int(input()) # количестов точек
r = 100 #int(input()) # радиус круга, внутри которого находятся находится большое скопление точек
c = 10 #int(input()) # на сколько частей разделятся данные для теста
Size = Data.get_Size() # размер поля НхН

""" 
    В программе используются два вида массивов с координатами точек:
    1. Двумерный массив для k-means: points[ точка - [координата х, координата у, номер группы (изначально -1)] ]
    2. Трехмерный массив для иерархии: array/part_of_data - [ группа - [ точка - [ координата х, координата у] ] ]
"""
#points = Data.generation(n,Size,False) # генерацияя случайных точек
points = Data.generation_in_groups(n,k,r,Size) # генерация случайных точек со скоплениями
#points = Data.generation_in_ring(n, Size // 10, Size*4 // 10, Size) # генерация вложенных точек
print("всего точек:", len(points))
Data.draw_points(points, False)
points = shuffle(points)
points_for_test = points[:(n//2)] # после перемешивания точек выбираем 1/2 часть для теста и для тренировки
points_for_train = points[(n//2):]
L = len(points_for_test)
q = L //  c # количество точек в выборке

centers = list()
for z in range(c+1):
    points_for_test = shuffle(points_for_test) # на каждой итерации перемешиваем старые точки
    points_for_test = points_for_test[L-q:] + points_for_train[(c-z)*q:] # убираем случайную десятую часть из страрых точек, поочередно добавляем каждую десятую часть из новых
    part_of_points = Data.random_part_of_array(points_for_test, q) # выбираем случайную десятую часть для выборки
    print("проводим иерархию на выборке:", q)
    new_centers, part_of_data = Fc.hierarchical(points_for_test[:q], Size) # получаем центры и массив с точками для иерархии

    conv_array = list()  # список точек в выпуклой оболочке
    for i in range(len(part_of_data)):
        S = Data.grahamscan(part_of_data[i]) # получение индексов точек в выпуклой оболочке
        conv_array.append(Data.convex_hull(S, part_of_data[i]))
        Data.draw_shell(conv_array[i]) # Построение выпуклой оболочки
    Nested = Fc.is_data_nested(new_centers, conv_array) # Проверка на вложенность

    if len(centers) != len(new_centers): # на каждой итерации выясняется, изменилось ли количество центров после прогона иерархии на очередной выборке
        print("Изменение центров: ", new_centers)
        centers = new_centers


    if Nested:
        print("Данные вложенные, запускаем hierarchical clustering")
        centers, array_of_data = Fc.hierarchical(points, Size)
    else:
        print("Данные не вложенные, запускаем k-means")
        centers, points_for_test = Fc.kmeans(points_for_test, centers, len(centers))

print(centers)
# centers = Data.generation(k, Size, True)  # генерация случайных центров