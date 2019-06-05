###############################################################################
# imports 
###############################################################################

# REQUIRED for c3
import qutip as qt
# FUTURE: import tensorflow as tf 
# REASON: tensorflow will become a hard requirement for c3 as certain 
#         functionality (i.e. GOAT) will depend on it


# import parts of c3 that are needed for the task at hand 
from c3po.main.gate import Gate as gt
from c3po.fidelity.measurement import Experiment as exp_backend


# optional/additional imports 
import matplotlib as plt  # for plotting
import os   # for interacting with operating system, i.e. creating files


###############################################################################
# connection to local experimental setup
#   
#   how is the data given by the optimizer transmitted to the local 
#   experimental setup?
###############################################################################

# EXAMPLE: communication via sockets

def create_socket():

    # PLACEHOLDER

    return 0


def send_data(socket, data):

    # PLACEHOLDER

    return 0


def read_data(socket):

    # PLACEHOLDER

    return 0


###############################################################################
# pulse specification
###############################################################################

# EXAMPLE

# Control1: c1 = A * cos(omega1 * t) + B * cos(omega2 * t)
#                   Carrier 1.1             Carrier 1.2
# Control2: c2 = C * cos(omega3 * t)
#                   Carrier 2.1
# =>    H = H0 + c1 * H1 + c2 * H2

# handmade_pulse = {
        # 'control1': {
            # 'carrier1': {
                # 'freq': 6e9*2*pi,
                # 'pulses': {
                    # 'pulse1': {
                        # 'amp': 15e6*2*pi,
                        # 't_up': 5e-9,
                        # 't_down': 45e-9,
                        # 'xy_angle': 0
                        # }
                    # }
                # }
            # }
        # }

initial_pulse = {

    # PLACEHOLDER 

}

# pulse_bounds = {
        # 'control1': {
            # 'carrier1': {
                # 'freq': [1e9*2*pi, 15e9*2*pi],
                # 'pulses': {
                    # 'pulse1': {
                        # 'amp':  [1e3*2*pi, 10e9*2*pi],
                        # 't_up': [2e-9, 98e-9],
                        # 't_down': [2e-9, 98e-9],
                        # 'xy_angle': [-pi, pi]
                        # }
                    # }
                # }
            # }
        # }


pulse_bounds = {

    # PLACEHOLDER

}

###############################################################################
# creation of gate object
#  
#   Represents a quantum gate with a fixed parametrization and envelope shape. 
###############################################################################

# EXAMPLE: Assume X_gate is target of operation

X_gate = gt('qubit_1', qt.sigmax())
X_gate.set_parameters('initial', initial_pulse)
X_gate.set_bounds(pulse_bounds)


###############################################################################
# evaluation function
#
#   Provide a function, specific to your experimental setup, that takes a 
#   several sets of parameters and provides a figure of merit for each.
###############################################################################

def evaluate_pulse(gate, samples):

    # PLACEHOLDER
    #   send pulses to experiment and receive output 

    infidelities = 0
    return infidelities



###############################################################################
# creation of experiment object 
#
#   driver for an experiment
#   
#   
###############################################################################

# EXAMPLE:

fridge = exp_backend(evaluate_pulse)


###############################################################################
# calibration
#
#
###############################################################################

# EXAMPLE:

# create paths for storing results of calibration process
data_path = "/tmp/c3_data/"
optim_name = data_path + "x_gate_calibration"
if not os.path.isdir(data_path):
    os.makedirs(data_path)
if not os.path.isdir(optim_name):
    os.makedirs(optim_name)


# change working path to 
ptim_name+"/"+time.strftime("%d%m%y-%H%M%S", time.localtime())
os.makedirs(pwd)

# input for function calibrate of Experiment obj 
opts = {
    'CMA_stds' : [1, 1, 1, 1, 1],
    'ftarget' : 1e-4,
    'popsize' : 20
}

# start calibration:
# Provide a gate to be calibrated with a gradient free search algorithm.
# At the moment this is CMA-ES and you can give valid opts

fridge.calibrate(X_gate, opts)

# Q: Incorporate Chalmers calibration?
#       - Nelder-Mead.py
#       - Bayesian-Gaussian-Process.py



