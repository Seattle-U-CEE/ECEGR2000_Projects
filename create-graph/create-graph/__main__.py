#!/usr/bin/python
#
# Description: Sample python code to create graph file
# from a Raspberry Pi
#
# Author: Eddy Ferre - ferree@seattleu.edu
#

from matplotlib import pyplot as plt
from numpy import linspace, exp, sin, pi


def main():
    try:

        # numpy methods (see https://numpy.org for more):
        # Define the x elements, here x = [-pi, pi], with 100 number of samples
        x = linspace(start=-pi, stop=pi, num=100)
        # Define the y elements, as a function of x
        y = sin(x)

        # matplotlib methods (see https://matplotlib.org for more):
        # create current axes and figure
        fig, ax = plt.subplots()
        # Plot y versus x as lines
        ax.plot(x, y)
        # Shows the axis grid
        ax.grid(visible=True, which='both')
        # Autoscale the axis view to the data
        ax.autoscale()
        # Save the current figure as an image or vector graphic to a file
        fig.savefig('singraph.jpeg')

    except KeyboardInterrupt:
        print()
        print("Exiting")
    except Exception as e:
        print(f'Exception: {e}')
    finally:
        pass


if __name__ == '__main__':
    main()