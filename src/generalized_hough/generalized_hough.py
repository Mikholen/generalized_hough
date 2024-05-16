"""generalized_hough module."""

from typing import Any, List, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np


def buildRefTable(img: np.ndarray) -> List[List[int]]:
    """Builds the reference table for the given input template image.

    Args:
        img (np.ndarray): Input binary image.

    Returns:
        List[List[int]]: A reconstructed reference table.
    """
    table = [[0 for x in range(1)] for y in range(90)]  # Creating an empty list
    # r will be calculated corresponding to this point
    img_center = [int(img.shape[0] / 2), int(img.shape[1] / 2)]

    def findAngleDistance(x1: int, y1: int) -> Tuple[int, Union[int, List[int]]]:
        """Finds angle distance.

        Args:
            x1 (int): x1.
            y1 (int): y1.

        Returns:
            Tuple[int, Union[int, List[int]]]: Angle distance table.
        """
        x2, y2 = img_center[0], img_center[1]
        r = [(x2 - x1), (y2 - y1)]
        if x2 - x1 != 0:
            return int(np.rad2deg(np.arctan(int((y2 - y1) / (x2 - x1))))), r
        else:
            return 0, 0

    filter_size = 3
    for x in range(img.shape[0] - (filter_size - 1)):
        for y in range(img.shape[1] - (filter_size - 1)):
            if img[x, y] != 0:
                theta, r = findAngleDistance(x, y)
                if r != 0:
                    table[np.absolute(theta)].append(r)

    for i in range(len(table)):
        table[i].pop(0)

    return table


def findMaxima(acc: np.ndarray) -> List[np.ndarray]:
    """Finds the maximum value in the accumulator array.

    Args:
        acc (np.ndarray): Accumulator array.

    Returns:
        List[int]: A list containing the maximum value found, row index,
                   and column index of the maximum value.

    """
    ridx, cidx = np.unravel_index(acc.ravel().argsort()[::-1][:1], acc.shape)
    return [acc[ridx, cidx], ridx, cidx]


def matchTable(im: np.ndarray, table: List[List[Any]]) -> np.ndarray:
    """Matches the reference table with the given input image.

    Args:
        im (np.ndarray): Input binary image, for searching template.
        table (List[List[Any]]): Table for template.

    Returns:
        np.ndarray: Accumulator with searched votes.
    """
    m, n = im.shape
    acc = np.zeros((m + 50, n + 50))  # Acc array requires some extra space

    def findGradient(x: int, y: int) -> int:
        if x != 0:
            return int(np.rad2deg(np.arctan(int(y / x))))
        else:
            return 0

    for x in range(1, im.shape[0]):
        for y in range(im.shape[1]):
            if im[x, y] != 0:  # Boundary point
                theta = findGradient(x, y)
                vectors = table[theta]
                for vector in vectors:
                    acc[vector[0] + x, vector[1] + y] += 1
    return acc


def main():
    """Generate an initial image, find detected lines,and display the results."""
    # Generating a horizontal line
    lines = np.zeros((250, 250))
    lines[40] = np.ones(250)
    plt.imshow(lines, cmap="gray")
    plt.title("Initial image")
    plt.show()

    images = [lines]
    for img in images:
        refim = img
        im = lines

        table = buildRefTable(refim)
        acc = matchTable(im, table)
        vals, ridxs, cidxs = findMaxima(acc)
        # Code for drawing bounding-box in accumulator array...

        for val, ridx, cidx in zip(vals, ridxs, cidxs):
            acc[ridx - 5 : ridx + 5, cidx - 5] = val
            acc[ridx - 5 : ridx + 5, cidx + 5] = val

            acc[ridx - 5, cidx - 5 : cidx + 5] = val
            acc[ridx + 5, cidx - 5 : cidx + 5] = val

        plt.imshow(acc, cmap="gray")
        plt.title("Accumulator array")
        plt.show()

        # Code for drawing bounding-box in original image
        # at the found location...

        # Find the half-width and height of the template
        hheight = np.floor(refim.shape[0] / 2) + 1
        hwidth = np.floor(refim.shape[1] / 2) + 1

        # Find coordinates of the box
        rstart = int(max(ridx - hheight, 1))
        rend = int(min(ridx + hheight, im.shape[0] - 1))
        cstart = int(max(cidx - hwidth, 1))
        cend = int(min(cidx + hwidth, im.shape[1] - 1))

        # Draw the box
        im[rstart:rend, cstart] = 0.5
        im[rstart:rend, cend] = 0.5

        im[rstart, cstart:cend] = 0.5
        im[rend, cstart:cend] = 0.5

        # Show the image
        plt.imshow(im, cmap="gray")
        plt.title("Detected lines")
        plt.show()


if __name__ == "__main__":
    main()
