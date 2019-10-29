"""Simulator."""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from c3po.model import Model
from c3po.control import GateSet
from c3po.generator import Generator

from c3po.tf_utils import tf_propagation as tf_propagation
from c3po.tf_utils import tf_propagation_lind as tf_propagation_lind
from c3po.tf_utils import tf_matmul_list as tf_matmul_list
from c3po.tf_utils import tf_super as tf_super


class Simulator():
    """Simulator object."""

    def __init__(self,
                 model: Model,
                 generator: Generator,
                 gateset: GateSet
                 # controls: GateSet
                 ):
        self.model = model
        self.generator = generator
        self.gateset = gateset

    def get_gates(
        self,
        model_params,
        gateset_values: list,
        opt_map: dict,
        lindbladian: bool = False
    ):
        gates = {}
        self.gateset.set_parameters(gateset_values, opt_map)
        # TODO allow for not passing model params
        # model_params, _ = self.model.get_values_bounds()
        for gate in self.gateset.instructions.keys():
            signal = self.generator.generate_signals(
                self.gateset.instructions[gate]
            )
            U = self.propagation(signal, model_params, lindbladian)
            gates[gate] = U
            if hasattr(self, 'VZ'):
                if lindbladian:
                    gates[gate] = tf_super(self.VZ) * gates[gate]
                else:
                    gates[gate] = self.VZ * gates[gate]
        return gates

    def evaluate_sequence(
        self,
        model_params: list,
        gateset_values: list,
        opt_map: dict,
        sequence: list,
        lindbladian: bool = False
    ):
        gates = self.get_gates(
            model_params,
            gateset_values,
            opt_map,
            lindbladian
        )
        Us = []
        for gate in sequence:
            Us.append(gates[gate])
        U = tf_matmul_list(Us)
        return U

    def propagation(self,
                    signal: dict,
                    model_params: list = None,
                    lindbladian: bool = False
                    ):
        signals = []
        # This sorting ensures that signals and hks are matched
        # TODO do hks and signals matching more rigorously
        for key in sorted(signal):
            out = signal[key]
            # TODO this points to the fact that all sim_res must be the same
            ts = out["ts"]
            signals.append(out["values"])

        dt = tf.cast(ts[1] - ts[0], tf.complex128, name="dt")
        h0, hks = self.model.get_Hamiltonians(model_params)
        if lindbladian:
            col_ops = self.model.get_lindbladian()
            dUs = tf_propagation_lind(h0, hks, col_ops, signals, dt)
        else:
            dUs = tf_propagation(h0, hks, signals, dt)
        self.dUs = dUs
        self.ts = ts
        U = tf_matmul_list(dUs)
        self.U = U
        return U

    def plot_dynamics(self,
                      psi_init,
                      lindbladian: bool = False
                      ):
        # TODO double check if it works well
        dUs = self.dUs
        psi_t = psi_init.numpy()
        pop_t = self.populations(psi_t, dv=lindbladian)
        for du in dUs:
            psi_t = np.matmul(du.numpy(), psi_t)
            pops = self.populations(psi_t, dv=lindbladian)
            pop_t = np.append(pop_t, pops, axis=1)
        fig, axs = plt.subplots(1, 1)
        ts = self.ts
        dt = ts[1] - ts[0]
        ts = np.append(0, ts + dt / 2)
        axs.plot(ts / 1e-9, pop_t.T)
        axs.grid()
        axs.set_xlabel('Time [ns]')
        axs.set_ylabel('Population')
        fig.show()

    @staticmethod
    def populations(state, dv=False):
        if dv:
            dim = int(np.sqrt(len(state)))
            indeces = [n * dim + n for n in range(dim)]
            return np.abs(state[indeces])
        else:
            return np.abs(state)**2
