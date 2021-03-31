# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2021, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

from torch.optim.lr_scheduler import LambdaLR


class LRRangeTestMixin:
    """
    Mixin for the LR-range test defined in section 4.1 of "A Disciplined Approach to
    Neural Network Hyper-Parameters"
        - https://arxiv.org/pdf/1803.09820.pdf

    Herein, a min_lr and max_lr are set, and training proceeds for a small number of
    epochs (1-3) while the learning rate is linearly or exponentially increased.
    Generally, the point at which the training loss begins to curve upwards, is
    considered to be a reasonable choice for your max_lr in a cyclical lr-schedule. For
    an exponential ramp-up, the ideal max_lr is roughly one order of magnitude below the
    point in which the loss begins to increase. The same author recommends using 10-20
    times lower this amount for your min_lr. Of course, in practice these heuristics may
    vary.

    :param min_lr: starting lr
    :param max_lr: ending lr; presumed to be larger than min_lr
    :param test_mode: either linear or exponential
    """
    def __init__(
        self,
        min_lr=None,
        max_lr=None,
        test_mode="linear",
        **kwargs,
    ):

        # The LambdaLR will multiply this base lr of 1 times the one at the given step.
        kwargs["args"].learning_rate = 1

        # Log so that the lr is recorder every step.
        kwargs["args"].logging_steps = 1

        # Turn off eval since it's satisfactory to just look at the training loss.
        kwargs["args"].do_eval = False

        super().__init__(**kwargs)
        assert isinstance(min_lr, float)
        assert isinstance(max_lr, float)
        assert test_mode in ["linear", "exponential"]
        self.min_lr = min_lr
        self.max_lr = max_lr
        self.test_mode = test_mode

    def create_optimizer_and_scheduler(self, num_training_steps: int):
        """
        Create a linearly or exponentially increasing lr schedule. This overrides super
        in a way that just customizes the lr scheduler while the optimizer remains the
        default.
        """

        # Set lr scheduler to dummy variable so it's not created in the call to super.
        self.lr_scheduler = ...

        # Create just the optimizer.
        super().create_optimizer_and_scheduler(num_training_steps)

        # Create a lr scheduler that ramps up either linearly or exponentially.
        total_steps = num_training_steps
        min_lr = self.min_lr
        max_lr = self.max_lr

        # Linearly increase lr
        if self.test_mode == "linear":
            def lr_lambda(step: int):
                return (max_lr - min_lr) / (total_steps - 1) * step + min_lr

        # Exponentially increase lr
        elif self.test_mode == "exponential":
            def lr_lambda(step):
                return (max_lr / min_lr) ** (step / (total_steps - 1)) * min_lr

        self.lr_scheduler = LambdaLR(self.optimizer, lr_lambda)
