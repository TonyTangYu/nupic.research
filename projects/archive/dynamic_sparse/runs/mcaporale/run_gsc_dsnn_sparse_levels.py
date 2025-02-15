# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2019, Numenta, Inc.  Unless you have an agreement
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

import os

import ray
import torch

from nupic.research.archive.dynamic_sparse.common.loggers import DEFAULT_LOGGERS
from nupic.research.archive.dynamic_sparse.common.utils import (
    Trainable,
    new_experiment,
    run_experiment,
)
from nupic.research.frameworks.pytorch.model_utils import set_random_seed

# Set seed for `random`, `numpy`, and `pytorch`.
set_random_seed(32)


def serializer(obj):
    if obj.is_cuda:
        return obj.cpu().numpy()
    else:
        return obj.numpy()


def deserializer(serialized_obj):
    return serialized_obj


# experiment configurations
base_exp_config = dict(
    device=("cuda" if torch.cuda.device_count() > 0 else "cpu"),
    # dataset related
    dataset_name="PreprocessedGSC",
    data_dir="~/nta/datasets/gsc",
    # batch_size_train=16,
    # batch_size_test=(1000),
    # # network related
    # network="GSCHeb",
    # # ----- Optimizer Related ----
    # optim_alg="SGD",
    # momentum=0.0,
    # learning_rate=0.01,
    # weight_decay=1e-2,
    # # ----- LR Scheduler Related ----
    # lr_scheduler="StepLR",
    # lr_step_size=1,
    # lr_gamma=0.9,
    batch_size_train=(4, 16),
    batch_size_test=1000,
    optim_alg="SGD",
    momentum=0,  # 0.9,
    learning_rate=0.01,  # 0.1,
    weight_decay=0.01,  # 1e-4,
    lr_scheduler="MultiStepLR",
    lr_milestones=[30, 60, 90],
    # lr_milestones=[30, 60, 90],
    lr_gamma=0.9,  # 0.1,
    # additional validation
    test_noise=False,
    # debugging
    debug_weights=True,
    debug_sparse=True,
)

# ray configurations
# experiment_name = "gsc-trials-2019-10-07"
# experiment_name = "gsc-dsnn-2019-10-11-G-reproduce"
experiment_name = "gsc-dsnn-2019-10-11-coact-plots-A"
tune_config = dict(
    name=experiment_name,
    num_samples=1,
    local_dir=os.path.expanduser(os.path.join("~/nta/results", experiment_name)),
    checkpoint_freq=0,
    checkpoint_at_end=False,
    stop={"training_iteration": 100},
    resources_per_trial={
        "cpu": os.cpu_count() / torch.cuda.device_count(),
        "gpu": 1,
    },
    loggers=DEFAULT_LOGGERS,
    verbose=1,
    config=base_exp_config,
)

# define experiments
net_params = dict(
    boost_strength=1.5,
    boost_strength_factor=0.9,
    k_inference_factor=1.5,
    duty_cycle_period=1000
)
on_perc_levels = [0.02, 0.04]  # , np.arange(0, 0.101, 0.005)
experiments = {

    # "gsc-Static": dict(
    #     model=ray.tune.grid_search(["SparseModel"]),
    #     network="gsc_sparse_dsnn",
    #     # sparse related
    #     on_perc=ray.tune.grid_search([
    #         [perc] * 4 for perc in
    #         on_perc_levels
    #     ]),
    # ),

    # "gsc-SET": dict(
    #     model=ray.tune.grid_search(["SET"]),
    #     network="gsc_sparse_dsnn",
    #     net_params=net_params,
    #     # network related
    #     prune_methods=[None, None, None, None],
    #     # sparse related
    #     on_perc=ray.tune.grid_search([
    #         [perc] * 4 for perc in
    #         on_perc_levels
    #     ]),
    #     hebbian_prune_perc=None,
    #     hebbian_grow=False,
    #     weight_prune_perc=[None, None, 0.3, 0.3],
    # ),

    # "gsc-WeightedMag": dict(
    #     model=ray.tune.grid_search(["DSNNWeightedMag"]),
    #     network="gsc_sparse_dsnn",
    #     net_params=net_params,
    #     # network related
    #     prune_methods=[None, None, "dynamic-linear", "dynamic-linear"],
    #     # sparse related
    #     on_perc=ray.tune.grid_search([
    #         [perc] * 4 for perc in
    #         on_perc_levels
    #     ]),
    #     hebbian_prune_perc=None,
    #     hebbian_grow=False,
    #     weight_prune_perc=[0.3, 0.3],
    # ),

    # ----------
    # Plots
    # ----------

    # "gsc-Static": dict(
    #     model=ray.tune.grid_search(["SparseModel"]),
    #     prune_methods=[None, None, "dynamic-linear", "dynamic-linear"],
    #     network="gsc_sparse_dsnn",
    #     # sparse related
    #     on_perc=ray.tune.grid_search([
    #         [0.02] * 4,
    #     ]),
    #     log_magnitude_vs_coactivations=True,
    #     track_coactivation_variants=True,
    # ),

    # "gsc-SET": dict(
    #     model=ray.tune.grid_search(["SET"]),
    #     network="gsc_sparse_dsnn",
    #     net_params=net_params,
    #     # network related
    #     prune_methods=[None, None, "dynamic-linear", "dynamic-linear"],
    #     # sparse related
    #     on_perc=ray.tune.grid_search([
    #         [0.02] * 4
    #     ]),
    #     hebbian_prune_perc=None,
    #     hebbian_grow=False,
    #     weight_prune_perc=[None, None, 0.3, 0.3],
    #     log_magnitude_vs_coactivations=True,
    #     track_coactivation_variants=True,
    # ),

    "gsc-WeightedMag": dict(
        model=ray.tune.grid_search(["DSNNWeightedMag"]),
        network="gsc_sparse_dsnn",
        net_params=net_params,
        # network related
        prune_methods=[None, None, "dynamic-linear", "dynamic-linear"],
        # sparse related
        on_perc=ray.tune.grid_search([
            [0.02] * 4
        ]),
        hebbian_prune_perc=None,
        hebbian_grow=False,
        weight_prune_perc=[0.3, 0.3],
        log_magnitude_vs_coactivations=True,
        track_coactivation_variants=True,
    ),

}
exp_configs = (
    [(name, new_experiment(base_exp_config, c)) for name, c in experiments.items()]
    if experiments
    else [(experiment_name, base_exp_config)]
)

# Register serializers.
ray.init()
for t in [
    torch.FloatTensor,
    torch.DoubleTensor,
    torch.HalfTensor,
    torch.ByteTensor,
    torch.CharTensor,
    torch.ShortTensor,
    torch.IntTensor,
    torch.LongTensor,
    torch.Tensor,
]:
    ray.register_custom_serializer(t, serializer=serializer, deserializer=deserializer)

# run all experiments in parallel
results = [
    run_experiment.remote(name, Trainable, c, tune_config) for name, c in exp_configs
]
ray.get(results)
ray.shutdown()
