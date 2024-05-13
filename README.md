# An implementation of Generalised Hough transform
## Description
GHT was developed to detect analytically defined shapes (e.g., line, circle, ellipse etc.). In these cases, we have knowledge of the shape and aim to find out its location and orientation in the image. The Generalized Hough Transform or GHT, introduced by Dana H. Ballard in 1981, is the modification of the Hough Transform using the principle of template matching. This modification enables the Hough Transform to be used for not only the detection of an object described with an analytic function. Instead, it can also be used to detect an arbitrary object described with its model.

## Steps
The steps involved in applying a GHT are as follows (in order):

- build reference table using the given reference image
- match table with original image
- find maximum points in the returned accumulator array

## Result
