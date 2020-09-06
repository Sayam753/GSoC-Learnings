"""Convergence criterion callbacks for VI."""

import collections
import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from typing import List, Optional
from tensorflow_probability.python.optimizer.convergence_criteria import convergence_criterion

ParameterState = collections.namedtuple("ParameterState", ["previous_value"])


def relative(current, prev, eps=1e-6):
    """Calculate relative tolerance."""
    return (tf.abs(current - prev) + eps) / (tf.abs(prev) + eps)


def absolute(current, prev):
    """Calculate absolute tolerance."""
    return tf.abs(current - prev)


_diff = dict(relative=relative, absolute=absolute)


class CheckParameterConvergence(convergence_criterion.ConvergenceCriterion):
    """Check convergence after certain number of iterations."""

    def __init__(
        self,
        every: int = 100,
        tolerance: float = 1e-3,
        diff: str = "relative",
        ord=np.inf,
        min_num_steps: int = 20,
        name: Optional[str] = None,
    ):

        self.every = every
        self.tolerance = tolerance
        self.diff = _diff[diff]
        self.ord = ord
        super(CheckParameterConvergence, self).__init__(
            min_num_steps=min_num_steps, name=name or "ParameterConvergence"
        )

    @staticmethod
    def flatten_params(params: List[tf.Tensor]) -> tf.Tensor:
        """Flattened view of parameters."""
        flattened_tensor = [tf.reshape(var, shape=[-1]) for var in params]
        return tf.concat(flattened_tensor, axis=0)

    def _bootstrap(self, loss, grads, parameters):
        del loss
        del grads
        return ParameterState(previous_value=self.flatten_params(parameters))

    def _one_step(self, step, loss, grads, parameters, auxiliary_state):
        del loss
        del grads
        return tf.cond(
            step % self.every == 0,
            lambda: tf.cond(
                tf.norm(
                    self.diff(self.flatten_params(parameters), auxiliary_state.previous_value),
                    self.ord,
                )
                < self.tolerance,
                lambda: (True, ParameterState(previous_value=self.flatten_params(parameters))),
                lambda: (False, ParameterState(previous_value=self.flatten_params(parameters))),
            ),
            lambda: (False, ParameterState(previous_value=auxiliary_state.previous_value)),
        )
