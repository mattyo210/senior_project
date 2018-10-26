# -*- coding: UTF-8 -*-
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
def map_plot():
    path = "data.txt"
    fig = plt.figure()
    with open(path) as f:
        # read from text
        s = f.read()
        # delete backet
        s = s.replace("],["," ")
        s = s.replace("[","")
        s = s.replace("]","")

        sp = s.split()
        x = []
        y = []
        for i in range(len(sp)):
            if (i % 2) == 0:
                x.append(float(sp[i]))
            else:
                y.append(float(sp[i]))

        plt.scatter(x,y)
        plt.show()

map_plot()
