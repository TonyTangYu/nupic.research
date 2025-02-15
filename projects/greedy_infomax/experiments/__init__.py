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

from .block_resnet50_optimization import CONFIGS as BLOCK_RESNET50
from .block_sparse_optimization import CONFIGS as BLOCK_SPARSE_OPTIMIZATION
from .block_wise_training import CONFIGS as BLOCK_WISE
from .default_base import CONFIGS as DEFAULT_BASE
from .linear_classification import CONFIGS as LINEAR_CLASSIFICATION
from .new_model import CONFIGS as NEW_MODEL
from .sigopt_experiments import CONFIGS as SIGOPT_EXPERIMENTS
from .small_sparse import CONFIGS as SMALL_SPARSE
from .sparse_resnets import CONFIGS as SPARSE_RESNETS

CONFIGS = dict()
CONFIGS.update(DEFAULT_BASE)
CONFIGS.update(SPARSE_RESNETS)
CONFIGS.update(SIGOPT_EXPERIMENTS)
CONFIGS.update(SMALL_SPARSE)
CONFIGS.update(BLOCK_WISE)
CONFIGS.update(LINEAR_CLASSIFICATION)
CONFIGS.update(BLOCK_SPARSE_OPTIMIZATION)
CONFIGS.update(BLOCK_RESNET50)
CONFIGS.update(NEW_MODEL)
