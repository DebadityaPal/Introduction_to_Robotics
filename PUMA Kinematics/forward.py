import math
import numpy as np


def make_transformation_matrix(table, i):

    a_i1 = table[i][1]
    alpha_i1 = math.radians(table[i][0])
    d_i = table[i][2]
    theta_i = math.radians(table[i][3])

    return np.array(
        [
            [math.cos(theta_i), -math.sin(theta_i), 0, a_i1],
            [
                math.cos(alpha_i1) * math.sin(theta_i),
                math.cos(alpha_i1) * math.cos(theta_i),
                -math.sin(alpha_i1),
                -d_i * math.sin(alpha_i1),
            ],
            [
                math.sin(alpha_i1) * math.sin(theta_i),
                math.sin(alpha_i1) * math.cos(theta_i),
                math.cos(alpha_i1),
                d_i * math.cos(alpha_i1),
            ],
            [0, 0, 0, 1],
        ]
    )


# Enter the number of joints here
joints = 6

print("Please enter the following parameters:")
table = np.zeros((joints, 4))
for i in range(joints):
    curr_parameter = np.array(
        [
            float(input("alpha{}: ".format(i))),
            float(input("a{}: ".format(i))),
            float(input("d{}: ".format(i + 1))),
            float(input("theta{}: ".format(i + 1))),
        ]
    )
    table[i] = curr_parameter
    print()

# Calculating the final tranformation matrix by multiplying the matrices one by one
T_final = make_transformation_matrix(table, 0)
for i in range(1, table.shape[0]):
    # @ stands for dot multiplication here
    T_final = T_final @ make_transformation_matrix(table, i)

end_effector_position = T_final @ np.array([0, 0, 0, 1])

print(
    "\nEnd effector position will be: ({}, {}, {})".format(
        end_effector_position[0], end_effector_position[1], end_effector_position[2]
    )
)
