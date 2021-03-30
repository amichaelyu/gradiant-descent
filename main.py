# CHANGE THESE #

"""
points for regression
in form [x,y]
"""
data = [[3, 5], [4, 8],[-2,6]]

"""
2 = linear
3 = quadratic
4 = cubic
"""
power = 3

"""
choose lower number for more accurate regressions, but slower run times
choose higher number for less accurate regressions, but faster run times
"""
a = 0.01

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


while fit != power:
    fit = 0
    for i in range(power):
        if theta[i] == oldTheta[i]:
            fit += 1
        oldTheta[i] = theta[i]
        tempTheta[i] = grad(theta, i, data)
    for i in range(power):
        theta[i] = tempTheta[i]

# printing
print("y = ", end="")
for i in range(power):
    if i + 1 != power:
        print(str(theta[i]) + " x^" + str(i) + " + ", end="")
    else:
        print(str(theta[i]) + " x^" + str(i), end="")
