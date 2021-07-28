
# extracted and adapted from Lenskit basic.py

class PopScore(Predictor):
    """
    Score items by their popularity.  Use with :py:class:`TopN` to get a
    most-popular-items recommender.
    Args:
        score_type(str):
            The method for computing popularity scores.  Can be one of the following:
            - ``'quantile'`` (the default)
            - ``'rank'``
            - ``'count'``
    Attributes:
        item_pop_(pandas.Series):
            Item popularity scores.
    """

    def __init__(self, score_method='quantile'):
        self.score_method = score_method

    def fit(self, ratings, **kwargs):
        _logger.info('counting item popularity')
        scores = ratings['item'].value_counts()
        if self.score_method == 'rank':
            _logger.info('ranking %d items', len(scores))
            scores = scores.rank().sort_index()
        elif self.score_method == 'quantile':
            _logger.info('computing quantiles for %d items', len(scores))
            cmass = scores.sort_values()
            cmass = cmass.cumsum()
            cdens = cmass / scores.sum()
            scores = cdens.sort_index()
        elif self.score_method == 'count':
            _logger.info('scoring items with their rating counts')
            scores = scores.sort_index()
        else:
            raise ValueError('invalid scoring method ' + repr(self.score_method))

        self.item_scores_ = scores

        return self

    def predict_for_user(self, user, items, ratings=None):
        return self.item_scores_.reindex(items)

    def __str__(self):
        return 'PopScore({})'.format(self.score_method)