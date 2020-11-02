import os
import numpy as np
import skimage.color as color
from skimage import io

def get_average_colors(img_names, N):
    X = np.zeros((len(img_names), N*3), dtype=np.float64) #features matrix

    for i in range(0, len(img_names)):
        red_sum = 0
        green_sum = 0
        blue_sum = 0 
        cnt = 0
        img = io.imread(img_names[i])
        size = len(img)

        # Divide the picture into several lines and count average RGB colors in each of them
        # N - lines quantity

        for j in range(0, N):
            for k in range((size//N)*j, (size//N)*(j+1)):
                for h in img[k]:
                    if h[0] > 30: 
                        c = h[0].tolist()
                        red_sum += c**2
                    if h[1] > 30: 
                        c = h[1].tolist()
                        blue_sum += c**2
                    if h[2] > 30: 
                        c = h[2].tolist()
                        green_sum += c**2
                    
                    #different types of preprocessing
                    #red_sum += h[0]
                    #blue_sum += h[1]
                    #green_sum += h[2]
                    #if h[0] > 30: red_sum += h[0]
                    #if h[1] > 30: blue_sum += h[1]
                    #if h[2] > 30: green_sum += h[2]
                    cnt += 1

            #count average color in each lines
            X[i, j*3] = red_sum / cnt
            X[i, j*3 + 1] = green_sum / cnt
            X[i, j*3 + 2] = blue_sum / cnt

            red_sum = 0
            green_sum = 0
            blue_sum = 0
            cnt = 0
    return X