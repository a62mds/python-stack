#!/usr/bin/env python3.5
# Generates a plot of runtimes of the Stack.min() method vs stack depth,
# demonstrating the O(1) performance of Stack.min()
from matplotlib import pyplot as plt
from matplotlib import ticker as tkr
import numpy as np
from random import random
from time import time

import stack


def gen_random_stack(depth):
    """Helper function that generates a Stack object of depth `depth`, with
    each stack frame holding a random real number in the range [0,1) generated
    using random.random()
    """
    if not depth >= 0:
        raise ValueError('Stack depth cannot be negative')
    return stack.Stack(random() for _ in range(depth))

def avg(seq):
    """Average value of the values in seq"""
    list_seq = list(seq)
    return sum(list_seq)/len(list_seq)

def avg_abs(seq):
    """Average of the absolute values of the values in seq"""
    return avg(map(abs, seq))


def timer(func, *args, **kwargs):
    """Simple function for determining the runtime of a function in seconds"""
    start = time()
    res = func(*args, **kwargs)
    end = time()
    return end - start

def min_method_timer(stack_depths):
    """Generates a list of stacks with depths specified in the argument
    `stack_depths` and returns the runtime of each stack's min() method
    """
    if not len(stack_depths) >= 1:
        raise ValueError('Need at least one Stack to check runtime of min')
    stacks = [gen_random_stack(depth) for depth in stack_depths]
    return [timer(stack.min) for stack in stacks]

def plot_min_method_runtimes(stack_depths):
    """Generate a list of runtimes of the min method called on Stacks of depths
    specified in `stack_depths` and plot the runtimes vs depths. Stack objects
    are all initialized within the function min_method_timer.
    """
    
    # Get list of runtimes
    min_runtimes = min_method_timer(stack_depths)

    # Compute the average of all but the first runtime (for some reason I haven't
    # quite figured out, the call to min on the first (shortest) stack always takes
    # much longer to run than successive calls on deeper stacks, hence the runtime
    # of the first call is not included in the computation of the average runtime)
    avg_runtime = avg(min_runtimes[1:])

    # Compute the maximum deviation from the average runtime
    max_deviation = max(abs(runtime - avg_runtime) for runtime in min_runtimes)

    # From matplotlib.pyplot.subplots() documentation:
    # Create a figure and a set of subplots
    # This utility wrapper makes it convenient to create common layouts of
    # subplots, including the enclosing figure object, in a single call.
    #   -> fig is a matplotlib.figure.Figure object
    #   -> ax is a matplotlib.axes.Axes object
    fig, ax = plt.subplots()

    # Define axis labels and apply to `ax`
    axes_labels = {'x' : '$\log_{10}($Stack depth$)$',
                   'y' : 'Runtime of Stack.min() method (s)'}
    ax.set_xlabel(axes_labels['x'])
    ax.set_ylabel(axes_labels['y'])

    # Define axis limits and apply to `ax`
    x_axis_limits = {'min' : min(np.log(stack_depths)) - 1,
                     'max' : max(np.log(stack_depths)) + 1}
    y_axis_limits = {'min' : avg_runtime - 1.1*max_deviation,
                     'max' : avg_runtime + 1.1*max_deviation}
    ax.set_xlim(x_axis_limits['min'], x_axis_limits['max'])
    ax.set_ylim(y_axis_limits['min'], y_axis_limits['max'])

    # Format the tick labels on the y-axis
    ax.yaxis.set_major_formatter(tkr.FuncFormatter(lambda x, p: '{:.3e}'.format(x)))

    # Plot the average runtime as horizontal line
    log_stack_depths = np.log(stack_depths)
    avg_runtime_list = [avg_runtime for _ in stack_depths]
    plt.plot(log_stack_depths, avg_runtime_list,
             linestyle='--', color='Red', label='Average runtime')

    # Plot the runtime of the min method vs stack depth
    plt.scatter(log_stack_depths, min_runtimes)

    ax.legend() # turn on legend
    ax.set_title('Runtime of Stack.min() method vs Stack depth')
    plt.show()

if __name__ == '__main__':
    stack_depths = [5**i for i in range(10)]
    plot_min_method_runtimes(stack_depths)
