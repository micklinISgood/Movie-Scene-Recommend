import os
from pyspark.mllib.recommendation import ALS

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_counts_and_averages(ID_and_ratings_tuple):
    """Given a tuple (movieID, ratings_iterable) 
    returns (movieID, (ratings_count, ratings_avg))
    """
    nratings = len(ID_and_ratings_tuple[1])
    return ID_and_ratings_tuple[0], (nratings, float(sum(x for x in ID_and_ratings_tuple[1]))/nratings)


class RecommendationEngine:
    """A movie recommendation engine
    """
    def parseRating(self,line):
        """
        Parses a rating record in MovieLens format userId::movieId::rating::timestamp .
        """
        fields = line.strip().split(",")
        return long(fields[3]) % 10, (int(fields[0]), int(fields[1]), float(fields[2]))
    
    def loadRatings(self,ratingsFile):
        """
        Load ratings from file.
        """
      
        f = open(ratingsFile, 'r')
        ratings = filter(lambda r: r[2] > 0, [self.parseRating(line)[1] for line in f])
        f.close()
        if not ratings:
            print "No ratings provided."
            sys.exit(1)
        else:
            return ratings
    def __count_and_average_ratings(self):
        """Updates the movies ratings counts from 
        the current data self.ratings_RDD
        """
        logger.info("Counting movie ratings...")
        movie_ID_with_ratings_RDD = self.ratings_RDD.map(lambda x: (x[1], x[2])).groupByKey()
        movie_ID_with_avg_ratings_RDD = movie_ID_with_ratings_RDD.map(get_counts_and_averages)
        self.movies_rating_counts_RDD = movie_ID_with_avg_ratings_RDD.map(lambda x: (x[0], x[1][0]))


    def __train_model(self):
        """Train the ALS model with the current dataset
        """
        logger.info("Training the ALS model...")
        self.model = ALS.train(self.ratings_RDD, self.rank, seed=self.seed,
                               iterations=self.iterations, lambda_=self.regularization_parameter)
        logger.info("ALS model built!")


    def __predict_ratings(self, user_and_movie_RDD):
        """Gets predictions for a given (userID, movieID) formatted RDD
        Returns: an RDD with format (movieTitle, movieRating, numRatings)
        """
        predicted_RDD = self.model.predictAll(user_and_movie_RDD)
        predicted_rating_RDD = predicted_RDD.map(lambda x: (x.product, x.rating))
        predicted_rating_title_and_count_RDD = \
            predicted_rating_RDD.join(self.movies_titles_RDD).join(self.movies_rating_counts_RDD)
        predicted_rating_title_and_count_RDD = \
            predicted_rating_title_and_count_RDD.map(lambda r: (r[1][0][1], r[1][0][0], r[1][1]))
        
        return predicted_rating_title_and_count_RDD
    
    def add_ratings(self, ratings):
        """Add additional movie ratings in the format (user_id, movie_id, rating)
        """
        # Convert ratings to an RDD
        new_ratings_RDD = self.sc.parallelize(ratings)
        # Add new ratings to the existing ones
        self.ratings_RDD = self.ratings_RDD.union(new_ratings_RDD)
        # Re-compute movie ratings count
        self.__count_and_average_ratings()
        # Re-train the ALS model with the new ratings
        self.__train_model()
        
        return ratings

    def get_ratings_for_movie_ids(self, user_id, movie_ids):
        """Given a user_id and a list of movie_ids, predict ratings for them 
        """
        requested_movies_RDD = self.sc.parallelize(movie_ids).map(lambda x: (user_id, x))
        # Get predicted ratings
        ratings = self.__predict_ratings(requested_movies_RDD).collect()

        return ratings

    def loadtxt(self):

        myRatings = self.loadRatings("myRating.txt")
        new_user_ID = 0
        print new_user_ID
        myRatingsRDD = self.sc.parallelize(myRatings)
        # print myRatings
        self.ratings_RDD = self.ratings_RDD.union(myRatingsRDD)
        self.__count_and_average_ratings()
        # Re-train the ALS model with the new ratings
        self.__train_model()
        new_user_ratings_ids = map(lambda x: x[1], myRatings) # get just movie IDs
        new_user_unrated_movies_RDD = (self.movies_RDD.filter(lambda x: x[0] not in new_user_ratings_ids).map(lambda x: (new_user_ID, x[0])))
        new_user_recommendations_RDD = self.model.predictAll(new_user_unrated_movies_RDD)
        new_user_recommendations_rating_RDD = new_user_recommendations_RDD.map(lambda x: (x.product, x.rating))
        new_user_recommendations_rating_title_and_count_RDD = \
        new_user_recommendations_rating_RDD.join(self.movies_titles_RDD).join(self.movies_genres).join(self.movies_rating_counts_RDD)
        print new_user_recommendations_rating_title_and_count_RDD.take(3)
        new_user_recommendations_rating_title_and_count_RDD = \
        new_user_recommendations_rating_title_and_count_RDD.map(lambda r: (r[1][0][0][1], r[1][0][0][0], r[1][0][1], r[1][1]))
        top_movies = new_user_recommendations_rating_title_and_count_RDD.filter(lambda r: r[2]>=25).takeOrdered(25, key=lambda x: -x[1])

        print ('TOP recommended movies (with more than 25 reviews):\n%s' %
            '\n'.join(map(str, top_movies)))
        return map(str, top_movies)


    def recommends(self, myRatings):

        
        new_user_ID = 0
        print new_user_ID
        myRatingsRDD = self.sc.parallelize(myRatings)
        # print myRatings
        self.ratings_RDD = self.ratings_init_RDD.union(myRatingsRDD)
        self.__count_and_average_ratings()
        # Re-train the ALS model with the new ratings
        self.__train_model()
        new_user_ratings_ids = map(lambda x: x[1], myRatings) # get just movie IDs
        new_user_unrated_movies_RDD = (self.movies_RDD.filter(lambda x: x[0] not in new_user_ratings_ids).map(lambda x: (new_user_ID, x[0])))
        new_user_recommendations_RDD = self.model.predictAll(new_user_unrated_movies_RDD)
        new_user_recommendations_rating_RDD = new_user_recommendations_RDD.map(lambda x: (x.product, x.rating))
        new_user_recommendations_rating_title_and_count_RDD = \
        new_user_recommendations_rating_RDD.join(self.movies_titles_RDD).join(self.movies_genres).join(self.movies_rating_counts_RDD)
        print new_user_recommendations_rating_title_and_count_RDD.take(3)
        new_user_recommendations_rating_title_and_count_RDD = \
        new_user_recommendations_rating_title_and_count_RDD.map(lambda r: (r[1][0][0][1], r[1][0][0][0], r[1][0][1], r[1][1]))
        top_movies = new_user_recommendations_rating_title_and_count_RDD.filter(lambda r: r[2]>=25).takeOrdered(25, key=lambda x: -x[1])

        print ('TOP recommended movies (with more than 25 reviews):\n%s' %
            '\n'.join(map(str, top_movies)))
        return map(str, top_movies)
    
    def get_top_ratings(self, user_id, movies_count):
        """Recommends up to movies_count top unrated movies to user_id
        """
        # Get pairs of (userID, movieID) for user_id unrated movies
        user_unrated_movies_rdd = self.ratings_RDD.filter(lambda rating: not rating[0] == user_id)\
                                                 .map(lambda x: (user_id, x[1])).distinct()
        # Get predicted ratings
        ratings = self.__predict_ratings(user_unrated_movies_RDD).filter(lambda r: r[2]>=25).takeOrdered(movies_count, key=lambda x: -x[1])

        return ratings

    def __init__(self, sc):
        """Init the recommendation engine given a Spark context and a dataset path
        """

        logger.info("Starting up the Recommendation Engine: ")

        self.sc = sc

        # Load ratings data for later use
        logger.info("Loading Ratings data...")
        # ratings_file_path = os.path.join(dataset_path, 'ratings.csv')
        ratings_raw_RDD = self.sc.textFile('ratings.csv')
        ratings_raw_data_header = ratings_raw_RDD.take(1)[0]
        self.ratings_RDD = ratings_raw_RDD.filter(lambda line: line!=ratings_raw_data_header)\
            .map(lambda line: line.split(",")).map(lambda tokens: (int(tokens[0]),int(tokens[1]),float(tokens[2]))).cache()
        self.ratings_init_RDD = self.ratings_RDD
        # Load movies data for later use
        logger.info("Loading Movies data...")
        # movies_file_path = os.path.join(dataset_path, 'movies.csv')
        movies_raw_RDD = self.sc.textFile('movies.csv')
        movies_raw_data_header = movies_raw_RDD.take(1)[0]
        print movies_raw_RDD.take(1)
        self.movies_RDD = movies_raw_RDD.filter(lambda line: line!=movies_raw_data_header)\
            .map(lambda line: line.split(",")).map(lambda tokens: (int(tokens[0]),tokens[1],tokens[2])).cache()
        print self.movies_RDD.take(3)
        self.movies_titles_RDD = self.movies_RDD.map(lambda x: (int(x[0]),x[1]))
        self.movies_genres = self.movies_RDD.map(lambda x: (int(x[0]),x[2]))
        # Pre-calculate movies ratings counts
        self.__count_and_average_ratings()

        # Train the model
        self.rank = 8
        self.seed = 5L
        self.iterations = 10
        self.regularization_parameter = 0.1
        self.__train_model() 
