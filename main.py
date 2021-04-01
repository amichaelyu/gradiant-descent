from manimlib import *
import numpy as np

# CHANGE THESE #

"""
points for regression
in form [x,y]
"""
data = [[-2, 2], [0, -2], [2, -1], [5, 2], [4, 3]]

"""
2 = linear
3 = quadratic
4 = cubic
"""
power = 2

"""
how many decimal points of accuracy you want
higher numbers may lead to longer run times
"""
dec = 6

"""
choose lower number for more accurate regressions, but slower run times
choose higher number for less accurate regressions, but faster run times
"""
a = 0.001

"""
chooses regression with highest r^2 value
won't go higher than higher power entered above
will include other types of regressions later on
"""
smart = False

# DONT CHANGE BELOW #

# whether the data fits or not
fit = 0

# training set size
m = len(data)

# theta
theta = []

# temp theta for simultaneous update
tempTheta = []

# old theta
oldTheta = []

# finals
fTheta = []

# adds items in to the list
if smart == False:
    for i in range(power):
        theta.append(0)
        tempTheta.append(0)
        oldTheta.append(1)


# hypothesis
def hypL(theta, x):
    n = 0
    for i in range(power):
        n += theta[i] * x ** i
    return n


# gradiant decent formula
def grad(theta, z, data):
    n = 0
    for i in range(m):
        n += (hypL(theta, data[i][0]) - data[i][1]) * data[i][0] ** z
    return theta[z] - a / m * n


def res(theta, data):
    predict = []
    mean = 0
    RSS = 0
    TSS = 0
    for i in data:
        temp = 0
        for z in range(len(theta)):
            temp += theta[z] * i[0] ** z
        predict.append(temp)
    for i in range(len(predict)):
        mean += predict[i]
    mean /= len(predict)
    for i in range(len(data)):
        RSS += (data[i][1] - predict[i]) ** 2
        TSS += (data[i][1] - mean) ** 2
    return 1 - RSS / TSS


if smart == True:
    fTheta.append([0, 0, 0])
    fTheta.append([0, 0, 0, 0])
    fTheta.append([0, 0, 0, 0, 0])
    for power in range(2, 5):
        for i in range(power):
            theta.append(0)
            tempTheta.append(0)
            oldTheta.append(1)
        while fit != power:
            fit = 0
            for i in range(power):
                if round(theta[i], dec) == round(oldTheta[i], dec):
                    fit += 1
                oldTheta[i] = theta[i]
                tempTheta[i] = grad(theta, i, data)
            for i in range(power):
                theta[i] = tempTheta[i]
        fTheta[power - 2][0] = res(theta, data)
        for i in range(power):
            fTheta[power - 2][i + 1] = theta[i]
        theta = theta[:-power]
        tempTheta = tempTheta[:-power]
        oldTheta = oldTheta[:-power]
    if fTheta[0][0] >= fTheta[1][0]:
        if fTheta[0][0] >= fTheta[2][0]:
            for i in range(2):
                theta.append(fTheta[0][i + 1])
                num = 2
        else:
            for i in range(4):
                theta.append(fTheta[2][i + 1])
                num = 3
    else:
        for i in range(3):
            theta.append(fTheta[1][i + 1])
            num = 4
    print("y = ", end="")
    for i in range(num):
        if i + 1 != num:
            print(str(round(theta[i], dec)) + " x^" + str(i) + " + ", end="")
        else:
            print(str(round(theta[i], dec)) + " x^" + str(i))
    print("r^2 = " + str(res(theta, data)))

else:
    # while fit != power:
    #     fit = 0
    #     for i in range(power):
    #         if round(theta[i], dec) == round(oldTheta[i], dec):
    #             fit += 1
    #         oldTheta[i] = theta[i]
    #         # print(theta[i])
    #         tempTheta[i] = grad(theta, i, data)
    #     for i in range(power):
    #         theta[i] = tempTheta[i]

    # printing
    print("y = ", end="")
    for i in range(power):
        if i + 1 != power:
            print(str(round(theta[i], dec)) + " x^" + str(i) + " + ", end="")
        else:
            print(str(round(theta[i], dec)) + " x^" + str(i))
    print("r^2 = " + str(res(theta, data)))


class animate(Scene):
    def construct(self):
        axes = Axes(
            # x-axis ranges from -1 to 10, with a default step size of 1
            x_range=(-6, 6, 1),
            # y-axis ranges from -2 to 10 with a step size of 0.5
            y_range=(-3, 3, 1),
            # The axes will be stretched so as to match the specified
            # height and width
            height=6,
            width=12,
            # Axes is made of two NumberLine mobjects.  You can specify
            # their configuration with axis_config
            axis_config={
                "stroke_color": GREY_A,
                "stroke_width": 2,
                "include_tip": False,
            },
            # Alternatively, you can specify configuration for just one
            # of them, like this.
        )
        axes.add_coordinate_labels()

        self.play(Write(axes, lag_ratio=0.01, run_time=1))

        # self.play(
        #     ShowCreation(sin_graph),
        #     FadeIn(sin_label, RIGHT),
        # )
        # self.wait(2)
        # self.play(
        #     ReplacementTransform(sin_graph, relu_graph),
        #     FadeTransform(sin_label, relu_label),
        # )

        # You can use axes.input_to_graph_point, abbreviated
        # to axes.i2gp, to find a particular point on a graph
        for i in range(len(data)):
            dot = Dot(color=RED)
            dot.move_to([data[i][0], data[i][1], 0])
            self.play(FadeIn(dot, scale=0.5))
        linear_graph1 = axes.get_graph(
            lambda x: 0,
            # use_smoothing=False,
            color=YELLOW,
        )
        linear_graph2 = axes.get_graph(
            lambda x: 0,
            # use_smoothing=False,
            color=YELLOW,
        )
        fit = 0
        last = 0
        num = 0
        rand = False
        iters = 1000
        while fit != power:
            fit = 0
            for i in range(power):
                if round(theta[i], dec) == round(oldTheta[i], dec):
                    fit += 1
                oldTheta[i] = theta[i]
                # print(theta[i])
                tempTheta[i] = grad(theta, i, data)
            for i in range(power):
                theta[i] = tempTheta[i]
            num += 1
            if round(num/iters) > last:
                if not rand:
                    linear_graph1 = axes.get_graph(
                        lambda x: theta[0] + theta[1] * x + theta[2],
                        # lambda x: theta[0] + theta[1] * x + theta[2] * x ** 2,
                        # lambda x: theta[0] + theta[1] * x + theta[2] * x ** 2 + theta[3] * x ** 3,
                        # use_smoothing=False,
                        color=YELLOW,
                    )
                    self.play(
                        ReplacementTransform(linear_graph2, linear_graph1),
                    )
                    rand = True
                    last = round(num / iters)
                else:
                    linear_graph2 = axes.get_graph(
                        lambda x: theta[0] + theta[1] * x + theta[2],
                        # lambda x: theta[0] + theta[1] * x + theta[2] * x ** 2,
                        # lambda x: theta[0] + theta[1] * x + theta[2] * x ** 2 + theta[3] * x ** 3,
                        # use_smoothing=False,
                        color=YELLOW,
                    )
                    self.play(
                        ReplacementTransform(linear_graph1, linear_graph2),
                    )
                    rand = False
                    last = round(num / iters)


        self.wait(5)
