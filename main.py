from manimlib import *
import numpy as np

# CHANGE THESE #
from manimlib.scene.vector_space_scene import VectorScene

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


class Decent(Scene):
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
        axes2 = Axes(
            # x-axis ranges from -1 to 10, with a default step size of 1
            x_range=(-3, 2, 1),
            # y-axis ranges from -2 to 10 with a step size of 0.5
            y_range=(-2, 4, 1),
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
        funcDx = lambda \
            x: -28053989 / 7054320 + 634631 / 4594590 * 2 * x + 9846547 / 26604864 * 3 * x ** 2 + -10202077 / 558702144 * 4 * x ** 3 + -5308757 / 931170240 * 5 * x ** 4 + 159751 / 399072960 * 6 * x ** 5
        func2 = lambda x: 2 * x ** 3 + x ** 4
        funcNP = lambda x: np.array([x * self.w / (self.xR * 2), func(x) * self.h / (self.yR * 2), 0])
        funcDxNP = lambda x, y: np.array([(x + y) * self.w / (self.xR * 2),
                                          func(x) * self.h / (self.yR * 2) + y * funcDx(x) * self.h / (self.yR * 2), 0])
        graph1 = axes.get_graph(
            func,
            # use_smoothing=False,
            color=WHITE,
        )
        self.play(ShowCreation(graph1))
        dot = Dot(color=RED)
        dot.move_to(funcNP(-1))
        path0 = axes.get_graph(func, x_range=[-1, 1.983])
        path1 = axes.get_graph(func, x_range=[-1, 0.5])
        path2 = axes.get_graph(func, x_range=[0.5, 1.5])
        path3 = axes.get_graph(func, x_range=[1.5, 1.75])
        path4 = axes.get_graph(func, x_range=[1.75, 1.983])
        # path2 = axes.get_graph(func, x_range=[-4, -5.665])
        # path2.reverse_points()
        # path3 = axes.get_graph(func2, x_range=[0, 1.3])
        # path3.reverse_points()

        gradArrow1 = Arrow(funcNP(-1), funcDxNP(-1, -3), color=RED)
        decArrow1 = Arrow(funcNP(-1), funcDxNP(-1, 3), color=RED)
        decArrow2 = Arrow(funcNP(0.5), funcDxNP(0.5, 3), color=RED)
        decArrow3 = Arrow(funcNP(1.5), funcDxNP(1.5, 3), color=RED)
        decArrow4 = Arrow(funcNP(1.75), funcDxNP(1.75, 3), color=RED)
        decArrow5 = Arrow(funcNP(1.983), funcDxNP(1.983, 3), color=RED)
        circle = Circle(arc_center=funcNP(1.983), radius=0.5, color=RED)

        self.wait(5)
        self.play(FadeIn(dot, scale=0.5))
        self.wait(5)
        self.play(MoveAlongPath(dot, path0), run_time=1)
        # self.play(ShowCreation(circle))
        self.wait(5)
        # self.play(FadeOut(circle))
        dot.move_to(funcNP(-1))
        self.wait(5)
        self.play(ShowCreation(gradArrow1))
        self.wait(5)
        self.play(Transform(gradArrow1, decArrow1))
        self.wait(5)
        self.play(FadeOut(gradArrow1))
        self.wait(5)
        self.play(MoveAlongPath(dot, path1), run_time=1)
        self.wait(1)
        self.play(ShowCreation(decArrow2))
        self.play(FadeOut(decArrow2))
        self.play(MoveAlongPath(dot, path2), run_time=1)
        self.wait(1)
        self.play(ShowCreation(decArrow3))
        self.play(FadeOut(decArrow3))
        self.play(MoveAlongPath(dot, path3), run_time=1)
        self.wait(1)
        self.play(ShowCreation(decArrow4))
        self.play(FadeOut(decArrow4))
        self.play(MoveAlongPath(dot, path4), run_time=1)
        self.wait(1)
        self.play(ShowCreation(decArrow5))
        self.play(FadeOut(decArrow5))
        self.wait(10)
        # dot.move_to(np.array([-4 * self.w / (self.xR * 2), func(-4) * self.h / (self.yR * 2), 0]))
        # self.wait()
        # self.play(MoveAlongPath(dot, path2), run_time=1)
        # self.wait(2)
        # self.play(FadeOut(dot))

        # graph2 = axes2.get_graph(
        #     func2,
        #     # use_smoothing=False,
        #     color=WHITE,
        # )
        # self.play(Transform(graph1, graph2))
        # dot.move_to([1.3 * self.w / 5, func2(1.3) * self.h / 6, 0])
        # self.play(FadeIn(dot))
        # self.wait()
        # self.play(MoveAlongPath(dot, path3), run_time=1)
        # self.wait(2)


class Text(Scene):
    def construct(self):
        text1 = TexText("Gradient")
        text2 = TexText("Accent")
        text3 = TexText("Descent")
        text4 = TexText("Gradient Descent")
        text1.to_edge(TOP)
        text2.to_edge(BOTTOM)
        text3.to_edge(BOTTOM)
        self.play(Write(text1))
        self.wait(5)
        self.play(Write(text2))
        self.wait(5)
        self.play(Transform(text2, text3))
        self.wait(5)
        textGroup = Group(text1, text2)
        self.play(Transform(textGroup, text4))
        self.wait(10)
