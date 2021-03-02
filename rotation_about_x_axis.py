import math

def rotate_and_translate():
    coord = list(
        map(
            int,
            input("Enter the point in x y z coordinates: ").strip().split(),
        )
    )[:3]
    theta = int(
        input(
            "Enter the angle in degrees by which the frame is rotated about the x-axis: "
        )
    )
    translation = list(
        map(
            int,
            input("Enter the amount of translation on each axis(x y z): ")
            .strip()
            .split(),
        )
    )[:3]

    transformation_matrix = [
        [1, 0, 0, translation[0]],
        [
            0,
            math.cos(math.radians(theta)),
            math.sin(math.radians(theta)),
            translation[1],
        ],
        [
            0,
            -1 * math.sin(math.radians(theta)),
            math.cos(math.radians(theta)),
            translation[2],
        ],
        [0, 0, 0, 1],
    ]

    coord.append(1)
    result = [0, 0, 0, 0]

    for elemX in range(len(result)):
        for elemY in range(len(transformation_matrix[elemX])):
            result[elemX] += transformation_matrix[elemX][elemY] * coord[elemY]
        

    print(f"Coordinates of Point {coord[0], coord[1], coord[2]} with respect to original frame is {result[0], result[1], result[2]}")
    input("Press Enter to exit...")

if __name__ == "__main__":
    rotate_and_translate()
