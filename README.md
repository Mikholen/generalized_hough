# An implementation of Generalised Hough transform
## Description
GHT was developed to detect analytically defined shapes (e.g., line, circle, ellipse etc.). In these cases, we have knowledge of the shape and aim to find out its location and orientation in the image. The Generalized Hough Transform or GHT, introduced by Dana H. Ballard in 1981, is the modification of the Hough Transform using the principle of template matching. This modification enables the Hough Transform to be used for not only the detection of an object described with an analytic function. Instead, it can also be used to detect an arbitrary object described with its model.

## Steps
The steps involved in applying a GHT are as follows (in order):

- build reference table using the given reference image
- match table with original image
- find maximum points in the returned accumulator array

## Result
### Initial image
![h](https://github.com/Mikholen/generalized_hough/assets/136765117/e3644223-82ac-4b45-8927-dc45bcf659bc)

### Maximum points in the returned accumulator array
![hh](https://github.com/Mikholen/generalized_hough/assets/136765117/2db658e7-87bb-4e25-8f0b-e352adf8b82e)

### Detected lines
![hhh](https://github.com/Mikholen/generalized_hough/assets/136765117/00911dfa-bd6b-4d00-810d-2e3d6bbdb872)


## Requirements
- Python 3.8 (or higher)

Libraries:
- Matplotlib
- Skimage
- Numpy
- Scipy

## How to run
Clone the respository:
```
git clone git@github.com:Mikholen/generalized_hough.git
cd generalized_hough
```
Execute the demo script:
```
python generalized_hough.py
```
## Documentation

The documentation for this project can be found in the `docs/_build/index.html` file. You can open this file in your web browser to view the detailed documentation, including usage instructions, API references, and examples.

## Nox Sessions

This project includes several [Nox](https://nox.thea.codes/en/stable/) sessions for automation tasks. You can use these sessions to perform various tasks such as linting, testing, type-checking, and building documentation.

To run Nox sessions, make sure you have [Nox](https://nox.thea.codes/en/stable/) installed. Then, execute the desired session by running the following command in your terminal:

```bash
nox -s session_name
```

### Available Sessions

- `typeguard`: Runtime type checking using Typeguard.
- `mypy`: Type-check using mypy.
- `tests`: Run the test suite.
- `lint`: Lint using flake8.
- `black`: Run black code formatter.
- `safety`: Scan dependencies for insecure packages.
- `pytype`: Type-check using pytype.
- `xdoctest`: Run examples with xdoctest.
- `docs`: Build the documentation.

For example, to run linting, execute:

```bash
nox -s lint
