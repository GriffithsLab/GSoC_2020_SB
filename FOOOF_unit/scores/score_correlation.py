# -*- coding: utf-8 -*-
"""Correlation Coefficient score class"""

import sciunit
import numpy as np

class CorrelationScore(sciunit.scores.Score):
    """A Correlation Score.

    A float in the range [-1.0,1.0] representing the correlation coefficient.
    """

    _description = ('A correlation of -1.0 shows a perfect negative correlation,'
                    'while a correlation of 1.0 shows a perfect positive correlation.'
                    'A correlation of 0.0 shows no linear relationship between the movement of the two variables')

    _best = 1.0

    def _check_score(self, score):
        if not (-1.0 <= score <= 1.0):
            raise errors.InvalidScoreError(("Score of %f must be in "
                                            "range -1.0-1.0" % score))
    @classmethod
    def compute(cls, observation, prediction):
        """Compute whether the observation equals the prediction."""
        return CorrelationScore(float(np.corrcoef(observation, prediction)[0,1]))

    def __str__(self):
        return '%.3g' % self.score
