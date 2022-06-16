from manimlib import *
import numpy as np

# CHANGE THESE #

"""
points for regression
in form [x,y]
"""
data = [[-1, -1], [0, 0], [1, 2], [-3, -6], [2, 7]]

"""
2 = linear
3 = quadratic
4 = cubic
"""
power = 4

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


class Animate(Scene):
    yR = 8
    xR = 12
    h = 7
    w = 13
    size = 20
    iters = 500

    def construct(self):
        axes = Axes(
            # x-axis ranges from -1 to 10, with a default step size of 1
            x_range=(-self.xR, self.xR, 1),
            # y-axis ranges from -2 to 10 with a step size of 0.5
            y_range=(-self.yR, self.yR, 1),
            # The axes will be stretched so as to match the specified
            # height and width
            height=self.h,
            width=self.w,
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

        textAnimate1 = Tex("y = 0\\\\r^2 = 0", font_size=self.size)
        self.play(Write(textAnimate1.to_edge(TOP).to_edge(LEFT)))

        # You can use axes.input_to_graph_point, abbreviated
        # to axes.i2gp, to find a particular point on a graph
        for i in range(len(data)):
            dot = Dot(color=RED)
            dot.move_to([data[i][0] * self.w / (self.xR * 2), data[i][1] * self.h / (self.yR * 2), 0])
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
            if round(num / self.iters) > last:
                if not rand:
                    linear_graph1 = axes.get_graph(
                        # lambda x: theta[0] + theta[1] * x,
                        # lambda x: theta[0] + theta[1] * x + theta[2] * x ** 2,
                        lambda x: theta[0] + theta[1] * x + theta[2] * x ** 2 + theta[3] * x ** 3,
                        # use_smoothing=False,
                        color=YELLOW,
                    )
                    self.play(
                        ReplacementTransform(linear_graph2, linear_graph1),
                    )
                    rand = True
                    last = round(num / self.iters)
                else:
                    linear_graph2 = axes.get_graph(
                        # lambda x: theta[0] + theta[1] * x,
                        # lambda x: theta[0] + theta[1] * x + theta[2] * x ** 2,
                        lambda x: theta[0] + theta[1] * x + theta[2] * x ** 2 + theta[3] * x ** 3,
                        # use_smoothing=False,
                        color=YELLOW,
                    )
                    self.play(
                        ReplacementTransform(linear_graph1, linear_graph2),
                    )
                    rand = False
                    last = round(num / self.iters)
                # text code
                text = "y = "
                for i in range(power):
                    if i + 1 != power:
                        text += (str(round(theta[i], dec)) + " x^" + str(i) + " + ")
                    else:
                        text += (str(round(theta[i], dec)) + " x^" + str(i))
                text += ("\\\\r^2 = " + str(res(theta, data)))
                textAnimate2 = Tex(text, font_size=self.size).to_edge(TOP).to_edge(LEFT)
                self.play(FadeTransform(textAnimate1, textAnimate2))
                textAnimate1 = textAnimate2


class Graph(Scene):
    yR = 15
    xR = 13
    h = 7
    w = 13
    size = 20
    iters = 500

    def construct(self):
        axes = Axes(
            # x-axis ranges from -1 to 10, with a default step size of 1
            x_range=(-self.xR, self.xR, 1),
            # y-axis ranges from -2 to 10 with a step size of 0.5
            y_range=(-self.yR, self.yR, 1),
            # The axes will be stretched so as to match the specified
            # height and width
            height=self.h,
            width=self.w,
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

        # You can use axes.input_to_graph_point, abbreviated
        # to axes.i2gp, to find a particular point on a graph
        func = lambda \
            x: -960389 / 554268 + -28053989 / 7054320 * x + 634631 / 4594590 * x ** 2 + 9846547 / 26604864 * x ** 3 + -10202077 / 558702144 * x ** 4 + -5308757 / 931170240 * x ** 5 + 159751 / 399072960 * x ** 6
        graph1 = axes.get_graph(
            func,
            # use_smoothing=False,
            color=YELLOW,
        )
        self.play(ShowCreation(graph1))
        dot = Dot(color=RED)
        dot.move_to([-1 * self.w / (self.xR * 2), func(-1) * self.h / (self.yR * 2), 0])
        path = axes.get_graph(func, x_range=[-1, 1.983])
        path2 = axes.get_graph(func, x_range=[-4, -5.665])
        path2.reverse_points()
        self.play(FadeIn(dot, scale=0.5))
        self.wait()
        self.play(MoveAlongPath(dot, path), run_time=1)
        self.wait(2)
        dot.move_to([-4 * self.w / (self.xR * 2), func(-4) * self.h / (self.yR * 2), 0])
        self.wait()
        self.play(MoveAlongPath(dot, path2), run_time=1)