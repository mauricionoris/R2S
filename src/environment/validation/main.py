# wrapper of all metrics to evaluate a recommendation

def main():

    from lenskit.datasets import MovieLens
    from lenskit.algorithms.bias import Bias
    from lenskit.batch import predict
    from lenskit.metrics.predict import user_metric, rmse
    ratings = MovieLens('/source/datasets/movielens/ml-latest-small').ratings.sample(frac=0.1)
    test = ratings.iloc[:1000]
    train = ratings.iloc[1000:]
    algo = Bias()
    algo.fit(train)
    preds = predict(algo, test)
    print(preds)
    x = user_metric(preds, metric=rmse)
    print(x)

if __name__ == '__main__':
    main()