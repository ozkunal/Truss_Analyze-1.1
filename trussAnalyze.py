# Libraries used in this project

import math
import numpy as np
import matplotlib.pyplot as plt

# Input area to define truss system parameters

elasticity = 1000  # Define Modulus of elasticity
areaSection = 8  # Define area of the sections
numOfJoints = 4  # Define total number of joints in the system
numOfMembers = 3  # Define total number of members in the system
np.set_printoptions(precision=5)  # Change the blue one to obtain desired precision for global stiffness matrix members

# Inputs to obtain members' location

listOfJoints = list(range(1, (numOfJoints * 2) + 1))
locationsOfPoints = []  # it defines the locations of the points in the truss
allPoints = []
allNodes = []

for i in range(numOfJoints):
    p = input(" enter the {}.joint NUMBER of the JOINT: ".format(i + 1))
    n1, n2 = input(" enter the NODE numbers of the {}.JOINT formatted as x,y: ".format(i + 1)).split(",")
    x, y = input("enter the LOCATION of the {}. JOINT formatted as x,y: ".format(i + 1)).split(",")
    points_ = [int(p)]
    nodes_ = [int(n1), int(n2)]
    location = (int(x), int(y))
    allPoints.extend(points_)
    allNodes.append(nodes_)
    locationsOfPoints.append(location)

# Establish progress of the members' identity properties

joints = list(range(1, numOfJoints + 1))
members = list(range(1, numOfMembers + 1))
nodes = [(i, i + 1) for i in range(1, (2 * numOfJoints) + 1, 2)]
jointNodeNumbers = list(zip(allPoints, allNodes))

jointIdentity = list(zip(allPoints, allNodes, locationsOfPoints))
jointIdentity = [list(x) for x in jointIdentity]

# Specifying degree of freedoms for the node numbers

constrainedNodes = []
loads = list()
displacements = list()

while True:
    constrained = input("enter a SINGLE constrained NODE NUMBER (for quit q): ")
    constrainedNodes.append(constrained)
    if constrained.lower() == "q":
        break

while True:
    load = input("enter a single LOAD and it's corresponding NODE NUMBER as (x,y) (for quit q): ")
    load_ = load.split(",")
    loads.append(load_)
    if load.lower() == "q":
        break

while True:
    displacement = input("enter a single DISPLACEMENT and it's corresponding NODE NUMBER as (x,y) (for quit q): ")
    displacement_ = displacement.split(",")
    displacements.append(displacement_)
    if displacement.lower() == "q":
        break

constrainedNodes.pop(-1)
loads.pop(-1)
displacements.pop(-1)
constrainedNodes = list(map(int, constrainedNodes))
loads.sort(key=lambda chain: chain[1])
displacements.sort(key=lambda ro: ro[1])

for t in range(len(constrainedNodes)):
    con_var = int(constrainedNodes[t])
    constrainedNodes[t] = con_var

for f in range(len(loads)):
    load_var = [float(loads[f][0]), int(loads[f][1])]
    loads[f] = load_var

for m in range(len(displacements)):
    disp_var = [float(displacements[m][0]), int(displacements[m][1])]
    displacements[m] = disp_var

for joint_ in listOfJoints:
    if joint_ not in constrainedNodes and joint_ not in [load1[1] for load1 in loads]:
        index = listOfJoints.index(joint_)
        loads.insert(index, [int(0), joint_])

for disp in listOfJoints:
    if disp not in constrainedNodes and disp not in [disp1[1] for disp1 in displacements]:
        ind_x = listOfJoints.index(disp)
        displacements.insert(ind_x, [f"d{disp}", disp])

# Creating known loads and known displacement matrices

upgraded_qk = list(np.zeros((2 * numOfJoints, 1)))
upgraded_dk = list(np.zeros((2 * numOfJoints, 1)))

for load_xen in loads:
    joint_index =\
        listOfJoints.index(load_xen[1])
    upgraded_qk[joint_index] = load_xen[0]

for disp_xx in displacements:
    jointIndex_ = listOfJoints.index(disp_xx[1])
    upgraded_dk[jointIndex_] = disp_xx[0]

# Drawing graph

points = {}

for index, element in enumerate(jointIdentity):
    points[allPoints[index]] = element[2]

# Calculating members' length,lambda values and drawing graph of the system

membersLengths = []
lambdaX = []
lambdaY = []


def calculate_distance(x_1, y_1, x_2, y_2):
    members_lengths = math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)
    return members_lengths


vectorInputs = []

for i in range(numOfMembers):
    point1, point2 = map(int, input(
        f"please select two joint from {joints} with dividing comma to draw a line between them : ").split(","))
    vectorInputs.append((point1, point2))
    x1, y1 = points[point1]
    x2, y2 = points[point2]
    plt.plot([x1, x2], [y1, y2], "-o", color="blue")
    plt.plot([x1, x2], [y1, y2], color="red")
    lengths = calculate_distance(x1, y1, x2, y2)
    membersLengths.append(lengths)
    lambda_x = round(((x2 - x1) / (membersLengths[i])), 4)
    lambda_y = round(((y2 - y1) / (membersLengths[i])), 4)
    lambdaX.append(lambda_x)
    lambdaY.append(lambda_y)

plt.show()

# Creating member stiffness matrices

membersStiffMtrx = []

for i in range(numOfMembers):
    k_values = np.array([lambdaX[i] ** 2, lambdaX[i] * lambdaY[i], -lambdaX[i] ** 2, -lambdaX[i] * lambdaY[i],
                         lambdaX[i] * lambdaY[i], lambdaY[i] ** 2, -lambdaX[i] * lambdaY[i], -lambdaY[i] ** 2,
                         -lambdaX[i] ** 2, -lambdaX[i] * lambdaY[i], lambdaX[i] ** 2, lambdaX[i] * lambdaY[i],
                         -lambdaX[i] * lambdaY[i], -lambdaY[i] ** 2, lambdaX[i] * lambdaY[i], lambdaY[i] ** 2])
    k = ((areaSection * elasticity) / membersLengths[i]) * k_values
    k = (np.array(k)).reshape(4, 4)
    membersStiffMtrx.append(k)

# Creating global stiffness matrix and its indices

globalStiffnessMatrix = np.zeros((numOfJoints * 2, numOfJoints * 2))

# Reshaping stiffness matrices according to the shape of global stiffness matrix

memberMtrxIdentity = []
memberMtrxIdentity1 = []
memberMtrxIdentity2 = []

for index, item in enumerate(jointNodeNumbers):
    for idx, element in enumerate(vectorInputs):
        if element[0] == item[0]:
            memberMtrxIdentity1.append([element, item[1]])

for index, item in enumerate(jointNodeNumbers):
    for idx, element in enumerate(vectorInputs):
        if element[1] == item[0]:
            memberMtrxIdentity2.append([element, item[1]])

for i in range(len(memberMtrxIdentity1)):
    for j in range(len(memberMtrxIdentity2)):
        if memberMtrxIdentity1[i][0] == memberMtrxIdentity2[j][0]:
            memberMtrxIdentity.append(
                [memberMtrxIdentity1[i][0], [memberMtrxIdentity1[i][1][0], memberMtrxIdentity1[i][1][1],
                                             memberMtrxIdentity2[j][1][0], memberMtrxIdentity2[j][1][1]]])

for i in range(len(vectorInputs)):
    for j in range(len(memberMtrxIdentity)):
        if vectorInputs[i] != memberMtrxIdentity[i][0]:
            if vectorInputs[i] == memberMtrxIdentity[j][0]:
                memberMtrxIdentity[i], memberMtrxIdentity[j] = memberMtrxIdentity[j], memberMtrxIdentity[i]

index_value_pairs = []
memberStiffnessValues = []

for i in range(numOfMembers):
    for j in range(len(membersStiffMtrx[i])):
        for k in range(len(membersStiffMtrx[i][0])):
            index_value_pairs.append([membersStiffMtrx[i][j][k], [j, k]])
            memberStiffnessValues.append([memberMtrxIdentity[i][1][j] - 1, memberMtrxIdentity[i][1][k] - 1])

index_value_pairs = [index_value_pairs[i:i + 16] for i in range(0, len(index_value_pairs), 16)]
memberStiffnessValues = [memberStiffnessValues[i:i + 16] for i in range(0, len(memberStiffnessValues), 16)]

for i in range(len(index_value_pairs)):
    for j in range(len(index_value_pairs[i])):
        index_value_pairs[i][j][1] = memberStiffnessValues[i][j]

# Finally editing the global stiffness matrix

for i in range(len(index_value_pairs)):
    for j in range(len(index_value_pairs[i])):
        globalStiffnessMatrix[index_value_pairs[i][j][1][0], index_value_pairs[i][j][1][1]] += \
            index_value_pairs[i][j][0]

# Specifying loads and displacements on the system

for i in range(len(upgraded_qk)):
    for j in range(len(upgraded_dk)):
        if type(upgraded_qk[i]) == int:
            upgraded_qk[i] = 0
        elif upgraded_qk[i] == np.array(0):
            upgraded_qk[i] = f"q{i + 1}"
        if upgraded_dk[j] == [[0.]]:
            upgraded_dk[j] = 0

# Arranging upgraded_qk and upgraded_qk

upgraded_qk = np.array(upgraded_qk, dtype=object).reshape(len(listOfJoints), 1)
upgraded_dk = np.array(upgraded_dk, dtype=object).reshape(len(listOfJoints), 1)

# Matrix partitioning

partition_num = len(listOfJoints) - len(constrainedNodes)
k_11, k_12 = np.split(globalStiffnessMatrix[:partition_num], [partition_num], axis=1)
k_21, k_22 = np.split(globalStiffnessMatrix[partition_num:], [partition_num], axis=1)
q_known, q_unknown = np.split(upgraded_qk, [partition_num])
d_unknown, d_known = np.split(upgraded_dk, [partition_num])
ku_disp = q_known - (k_12 @ d_known)
disp_val = np.linalg.inv(k_11) @ ku_disp
load_val = k_21 @ disp_val + k_22 @ d_known
disp_val_last = []
load_val_last = []

for i in range(len(d_unknown)):
    disp_val_last.append([d_unknown[i][0], round(disp_val[i][0], 5)])

for j in range(len(q_unknown)):
    load_val_last.append([q_unknown[j][0], round(load_val[j][0], 3)])

# Defining member compression / tension situations

all_disp = []
all_loads = []

all_disp += disp_val_last

for i in range(partition_num, len(upgraded_dk)):
    if upgraded_dk[i][0] == 0:
        all_disp.append([f"d{i + 1}", upgraded_dk[i][0]])
    else:
        all_disp.append([upgraded_dk[i][0], 0])

for i in range(partition_num):
    all_loads.append([f"q{i + 1}", upgraded_qk[i][0]])

all_loads += load_val_last
nf_val = []

for i in range(len(all_disp)):
    if type(all_disp[i][0]) == float:
        all_disp[i][0], all_disp[i][1] = all_disp[i][1], all_disp[i][0]
        all_disp[i][0] = f"d{i + 1}"

for k in range(numOfMembers):
    for item in memberMtrxIdentity[k][1]:
        for j in range(len(all_disp)):
            if str(item) in all_disp[j][0]:
                if item == int(all_disp[j][0][1:]):
                    nf_val.append(all_disp[j][1])

nf_val = [nf_val[i:i + 4] for i in range(0, len(nf_val), 4)]
lamda_values = []

for i in range(numOfMembers):
    lamda_values.append([i + 1, [lambdaX[i], lambdaY[i]]])

lambda_for_force = []

for i in range(len(lamda_values)):
    lambda_for_force.append([-lamda_values[i][1][0], -lamda_values[i][1][1],
                             lamda_values[i][1][0], lamda_values[i][1][1]])

member_forces = []

for i in range(numOfMembers):
    member_forces.append(((areaSection * elasticity) / membersLengths[i]) * np.dot(
        np.array(lambda_for_force[i]).reshape(1, 4), np.array(nf_val[i]).reshape(4, 1)))

print("global Stiffness Matrix: ", globalStiffnessMatrix)
print("displacements: ")

for i in range(len(disp_val_last)):
    print(f"{disp_val_last[i][0]} :", disp_val_last[i][1])

print("loads: ")

for i in range(len(load_val_last)):
    print(f"{load_val_last[i][0]} :", load_val_last[i][1])

print("member forces: ")

for i in range(len(member_forces)):
    print(f"member{i + 1} :", round(member_forces[i][0][0], 3))
