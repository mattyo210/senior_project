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

        print ("choose data format 0.(x,y x,y ...) 1.(x,x,x... y,y,y...) ->")
        Input = input()
        x = []
        y = []
        if Input == 0:
            s = s.replace("],["," ")
            s = s.replace("[","")
            s = s.replace("]","")
            sp = s.split()
            for i in range(len(sp)):
                if (i % 2) == 0:
                    x.append(float(sp[i]))
                else:
                    y.append(float(sp[i]))

        elif Input == 1:
            s = s.replace("],["," , ")
            s = s.replace("[","")
            s = s.replace("]"," ]")
            sp = s.split()
            count = 0
            for i in range(len(sp)):
                if sp[i] == "]":
                    count = count + 1
            j = 0
            for i in range(count):
                while sp[j] != ",":
                    x.append(sp[j])
                    j = j + 1
                while sp[j] != "]":
                    y.append(sp[j])
                    j = j + 1
            b = x[325]
            for i in range(x.count(x[325])):
                x.remove(b)
            for i in range(len(x)):
                x[i] = float(x[i])
            a = y[0]
            for i in range(y.count(y[0])):
                y.remove(a)
            for i in range(len(y)):
                y[i] = float(y[i])
        plt.scatter(x,y,s = 0.4)
        plt.show()

map_plot()
