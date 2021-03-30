# CHANGE THESE #

"""
points for regression
in form [x,y]
"""
data = [[3, 5], [4, 8], [-2,6], [1,2]]

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
dec = 5

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

# adds items in to the list
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
        RSS += (data[i][1] - predict[i])**2
        TSS += (data[i][1] - mean)**2
    return 1-RSS/TSS

while fit != power:
    fit = 0
    for i in range(power):
        if round(theta[i],dec) == round(oldTheta[i],dec):
            fit += 1
        oldTheta[i] = theta[i]
        tempTheta[i] = grad(theta, i, data)
    for i in range(power):
        theta[i] = tempTheta[i]

# printing
print("y = ", end="")
for i in range(power):
    if i + 1 != power:
        print(str(round(theta[i], dec)) + " x^" + str(i) + " + ", end="")
    else:
        print(str(round(theta[i], dec)) + " x^" + str(i))
print("r^2 = " + str(res(theta, data)))