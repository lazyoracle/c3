"""Object that deals with the sensitivity test."""

import os
from c3.optimizers.c3 import C3


class SET(C3):
    """Object that deals with the sensitivity test.

    Parameters
    ----------
    dir_path : str
        Filepath to save results
    fom : callable
        Figure of merit
    sampling : str
        Sampling method from the sampling library
    batch_sizes : list
        Number of points to select from each dataset
    sweep_map : list
        Identifiers to be swept
    state_labels : list
        Identifiers for the qubit subspaces
    algorithm : callable
        From the algorithm library
    options : dict
        Options to be passed to the algorithm
    same_dyn : boolean
        ?
    run_name : str
        User specified name for the run, will be used as root folder
    """

    def __init__(
        self,
        estimator,
        estimator_list,
        sampling,
        batch_sizes,
        pmap,
        datafiles,
        dir_path=None,
        state_labels=None,
        sweep_map=None,
        sweep_bounds=None,
        algorithm=None,
        run_name=None,
        same_dyn=False,
        options={},
    ):
        """Initiliase."""

        super().__init__(
            sampling,
            batch_sizes,
            pmap,
            datafiles,
            dir_path,
            state_labels=state_labels,
            algorithm=algorithm,
            run_name=run_name,
            options=options,
        )
        self.sweep_map = sweep_map
        self.pmap.opt_map = [sweep_map[0]]
        self.sweep_bounds = sweep_bounds
        self.run = self.sensitivity  # alias for legacy method

    def sensitivity(self):
        """
        Run the sensitivity analysis.

        """
        for ii in range(len(self.sweep_map)):
            self.pmap.opt_map = [self.sweep_map[ii]]
            self.options["bounds"] = [self.sweep_bounds[ii]]
            print(f"C3:STATUS:Sweeping {self.pmap.opt_map}: {self.sweep_bounds[ii]}")
            self.log_setup()
            self.start_log()
            print(f"C3:STATUS:Saving as: {os.path.abspath(self.logdir + self.logname)}")
            x_init = self.pmap.get_parameters_scaled()
            try:
                self.algorithm(
                    x_init,
                    fun=self.fct_to_min,
                    fun_grad=self.fct_to_min_autograd,
                    grad_lookup=self.lookup_gradient,
                    options=self.options,
                )
            except KeyboardInterrupt:
                pass
