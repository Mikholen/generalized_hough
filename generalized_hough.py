import numpy as np
from scipy.ndimage import convolve
from skimage import io
import matplotlib.pyplot as plt


def buildRefTable(img):
    """
    builds the reference table for the given input template image
    :param im: input binary image
    :return:
        table = a reconstructed reference table...
    """
    table = [[0 for x in range(1)] for y in range(90)]  # creating a empty list
    # r will be calculated corresponding to this point
    img_center = [int(img.shape[0]/2), int(img.shape[1]/2)]

    def findAngleDistance(x1, y1):
        x2, y2 = img_center[0], img_center[1]
        r = [(x2-x1), (y2-y1)]
        if (x2-x1 != 0):
            return [int(np.rad2deg(np.arctan(int((y2-y1)/(x2-x1))))), r]
        else:
            return [0, 0]

    filter_size = 3
    for x in range(img.shape[0]-(filter_size-1)):
        for y in range(img.shape[1]-(filter_size-1)):
            if (img[x, y] != 0):
                theta, r = findAngleDistance(x, y)
                if (r != 0):
                    table[np.absolute(theta)].append(r)

    for i in range(len(table)):
        table[i].pop(0)

    return table

def findMaxima(acc):
    """
    :param acc: accumulator array
    :return:
        maxval: maximum value found
        ridx: row index of the maxval
        cidx: column index of the maxval
    """
    ridx, cidx = np.unravel_index(acc.ravel().argsort()[::-1][:1], acc.shape)
    return [acc[ridx, cidx], ridx, cidx]


def matchTable(im, table):
    """
    :param im: input binary image, for searching template
    :param table: table for template
    :return:
        accumulator with searched votes
    """
    # matches the reference table with the given input
    # image for testing generalized Hough Transform
    m, n = im.shape
    acc = np.zeros((m+50, n+50))  # acc array requires some extra space

    def findGradient(x, y):
        if (x != 0):
            return int(np.rad2deg(np.arctan(int(y/x))))
        else:
            return 0

    for x in range(1, im.shape[0]):
        for y in range(im.shape[1]):

            if im[x, y] != 0:  # boundary point
                theta = findGradient(x, y)
                vectors = table[theta]
                for vector in vectors:
                    acc[vector[0]+x, vector[1]+y] += 1
    return acc

def main():

    #generating horizontal line
    lines = np.zeros((250, 250))
    lines[40] = np.ones(250)
    plt.imshow(lines, cmap='gray')
    plt.title('Initial image')
    plt.show()


    images = [lines]
    for img in images:
        refim = img
        im = lines

        table = buildRefTable(refim)
        acc = matchTable(im, table)
        val, ridx, cidx = findMaxima(acc)
        # code for drawing bounding-box in accumulator array...

        for val, ridx, cidx in zip(val, ridx, cidx):
            acc[ridx - 5:ridx + 5, cidx - 5] = val
            acc[ridx - 5:ridx + 5, cidx + 5] = val

            acc[ridx - 5, cidx - 5:cidx + 5] = val
            acc[ridx + 5, cidx - 5:cidx + 5] = val


        plt.imshow(acc, cmap='grey')
        plt.title('Accumulator array')
        plt.show()

        # code for drawing bounding-box in original image at the found location...

        # find the half-width and height of template
        hheight = np.floor(refim.shape[0] / 2) + 1
        hwidth = np.floor(refim.shape[1] / 2) + 1

        # find coordinates of the box
        rstart = int(max(ridx - hheight, 1))
        rend = int(min(ridx + hheight, im.shape[0] - 1))
        cstart = int(max(cidx - hwidth, 1))
        cend = int(min(cidx + hwidth, im.shape[1] - 1))

        # draw the box
        im[rstart:rend, cstart] = 0.5
        im[rstart:rend, cend] = 0.5

        im[rstart, cstart:cend] = 0.5
        im[rend, cstart:cend] = 0.5

        # show the image
        # plt.imshow(refim, cmap='grey')
        # plt.show()
        plt.imshow(im, cmap='grey')
        plt.title('Detected lines')
        plt.show()

if __name__ == '__main__':
    main()