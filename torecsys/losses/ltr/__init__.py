r"""torecsys.losses.ltr is a sub module of implementation of losses in learning-to-rank.
"""

from .. import _Loss


class _RankingLoss(_Loss):
    def __init__(self):
        super(_RankingLoss, self).__init__()


from .functional import *
from .groupwise_ranking_loss import *
from .pointwise_ranking_loss import *
from .pairwise_ranking_loss import *
