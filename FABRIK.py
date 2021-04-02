import math
import sys

import numpy as np


class Fabrik:
    def __init__(self, joint_positions, tolerance: float):
        if tolerance <= 0:
            raise ValueError("tolerance must be > 0")
        self.joints = joint_positions
        self.tolerance: float = tolerance
        self.link_lengths = []

        joint_a = joint_positions[0]
        for joint_b in joint_positions[1:]:
            self.link_lengths.append(np.linalg.norm(joint_a - joint_b))
            joint_a = joint_b

        if any([ll <= 0 for ll in self.link_lengths]):
            raise ValueError("link lengths must be > 0")

        self.lengths = self.link_lengths
        self.max_len = sum(self.link_lengths)

        self._has_moved = True
        self._angles = []
        _ = self.angles

    def as_length(self, vector, length):
        return vector * length / np.linalg.norm(vector)

    def angles(self):
        if not self._has_moved:
            return self._angles

        angles = [math.atan2(self.joints[1][1], self.joints[1][0])]

        prev_angle: float = angles[0]
        for i in range(2, len(self.joints)):
            p = self.joints[i] - self.joints[i - 1]
            abs_angle: float = math.atan2(p[1], p[0])
            angles.append(abs_angle - prev_angle)
            prev_angle = abs_angle

        self.has_moved = False
        self._angles = angles
        return self._angles

    def solvable(self, target):
        return self.max_len >= np.linalg.norm(target)

    def angles_deg(self):
        angles = self.angles()
        angles = [math.degrees(val) for val in angles]
        return angles

    def move_to(self, target, try_to_reach=True):
        if not self.solvable(target):
            if not try_to_reach:
                return 0
            target = self.as_length(target, self.max_len)
        return self._iterate(target)

    def _iterate(self, target):
        iteration: int = 0
        initial_position = self.joints[0]
        last: int = len(self.joints) - 1

        while np.linalg.norm(self.joints[-1] - target) > self.tolerance:
            iteration += 1

            self.joints[-1] = target
            for i in reversed(range(0, last)):
                next, current = self.joints[i + 1], self.joints[i]
                len_share = self.lengths[i] / np.linalg.norm(next - current)
                self.joints[i] = (1 - len_share) * next + len_share * current

            self.joints[0] = initial_position
            for i in range(0, last):
                next, current = self.joints[i + 1], self.joints[i]
                len_share = self.lengths[i] / np.linalg.norm(next - current)
                self.joints[i + 1] = (1 - len_share) * current + len_share * next
        return iteration


if __name__ == "__main__":

    coord1 = list(
        map(
            int,
            input("Enter first coordinate: ").strip().split(),
        )
    )[:3]

    coord2 = list(
        map(
            int,
            input("Enter second coordinate: ").strip().split(),
        )
    )[:3]

    coord3 = list(
        map(
            int,
            input("Enter third coordinate: ").strip().split(),
        )
    )[:3]

    coord4 = list(
        map(
            int,
            input("Enter fourth coordinate: ").strip().split(),
        )
    )[:3]

    tolerance = float(input("Enter Tolerance: "))

    goal = list(
        map(
            int,
            input("Enter goal coordinate: ").strip().split(),
        )
    )[:3]

    intial_coord = [
        np.array(coord1),
        np.array(coord2),
        np.array(coord3),
        np.array(coord4),
    ]
    initial_pos = intial_coord
    fab = Fabrik(intial_coord, tolerance)

    iterations = fab.move_to(np.array(goal))
    print("------Results------")
    print("Iterations: ", iterations)
    print("Angles:", fab.angles_deg())
    print("Link position:", fab.joints)
    print("Goal Position:", goal)