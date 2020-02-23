from c3po.c3objs import C3obj, Quantity
import tensorflow as tf
import c3po.libraries.constants as constants
import c3po.utils.tf_utils as tf_utils
import c3po.utils.qt_utils as qt_utils


class Task(C3obj):
    """Task that is part of the measurement setup."""

    def __init__(
            self,
            name: str = " ",
            desc: str = " ",
            comment: str = " ",
    ):
        super().__init__(
            name=name,
            desc=desc,
            comment=comment
        )


class InitialiseGround(Task):
    """Initialise the ground state with a given thermal distribution."""

    def __init__(
            self,
            name: str = "init_ground",
            desc: str = " ",
            comment: str = " ",
            init_temp: Quantity = None
    ):
        super().__init__(
            name=name,
            desc=desc,
            comment=comment
        )
        self.params['init_temp'] = init_temp

    def initialise(self, drift_H, lindbladian):
        init_temp = tf.cast(
            self.params['init_temp'].get_value(), dtype=tf.complex128
        )
        diag = tf.linalg.diag_part(drift_H)
        dim = len(diag)
        if init_temp:  # this checks that it's not zero
            # TODO Deal with dressed basis for thermal state
            freq_diff = diag - diag[0]
            beta = 1 / (init_temp * constants.kb)
            det_bal = tf.exp(-constants.hbar * freq_diff * beta)
            norm_bal = det_bal / tf.reduce_sum(det_bal)
            state = tf.reshape(tf.sqrt(norm_bal), [norm_bal.shape[0], 1])
        else:
            state = tf.constant(
                qt_utils.basis(dim, 0),
                shape=[dim, 1],
                dtype=tf.complex128
            )
        if lindbladian:
            return tf_utils.tf_dm_to_vec(tf_utils.tf_state_to_dm(state))
        else:
            return state


class ConfusionMatrix(Task):
    """Do confused assignment."""

    def __init__(
            self,
            name: str = "conf_matrix",
            desc: str = " ",
            comment: str = " ",
            confusion_row: Quantity = None
    ):
        super().__init__(
            name=name,
            desc=desc,
            comment=comment
        )
        self.params['confusion_row'] = confusion_row

    def pop1(self, pops, lindbladian):
        if 'confusion_row' in self.params:
            row1 = self.params['confusion_row'].get_value()
            row2 = tf.ones_like(row1) - row1
            conf_matrix = tf.concat([[row1], [row2]], 0)
        elif 'confusion_matrix' in self.params:
            conf_matrix = self.params['confusion_matrix'].get_value()
        pops = tf.reshape(pops, [pops.shape[0], 1])
        pop1 = tf.matmul(conf_matrix, pops)[1]
        return pop1


class MeasurementRescale(Task):
    """Rescale the result of the measurements."""

    def __init__(
            self,
            name: str = "meas_rescale",
            desc: str = " ",
            comment: str = " ",
            meas_offset: Quantity = None,
            meas_scale: Quantity = None,
    ):
        super().__init__(
            name=name,
            desc=desc,
            comment=comment
        )
        self.params['meas_offset'] = meas_offset
        self.params['meas_scale'] = meas_scale

    def rescale(self, pop1):
        pop1 = pop1 * self.params['meas_scale'].get_value()
        pop1 = pop1 + self.params['meas_offset'].get_value()
        return pop1