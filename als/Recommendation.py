
# coding: utf-8

# In[1]:

small_dataset_url = 'http://files.grouplens.org/datasets/movielens/ml-latest-small.zip'


# In[2]:

import os
datasets_path = os.path.join('..','Project','datasets')
small_dataset_path = os.path.join(datasets_path, 'ml-latest-small.zip')


# In[3]:

import urllib

small_f = urllib.urlretrieve (small_dataset_url, small_dataset_path)


# In[4]:

import zipfile

with zipfile.ZipFile(small_dataset_path, "r") as z:
    z.extractall(datasets_path)


# In[5]:

from pyspark import SparkContext
from pyspark import SparkConf


# In[6]:

conf = SparkConf().setMaster("local").setAppName("test_data")
sc = SparkContext(conf=conf)


# In[7]:


small_ratings_file = os.path.join(datasets_path, 'ml-latest-small', 'ratings.csv')

small_ratings_raw_data = sc.textFile(small_ratings_file)
small_ratings_raw_data_header = small_ratings_raw_data.take(1)[0]


# In[8]:

small_ratings_data = small_ratings_raw_data.filter(lambda line: line!=small_ratings_raw_data_header)    .map(lambda line: line.split(",")).map(lambda tokens: (tokens[0],tokens[1],tokens[2])).cache()


# In[9]:

small_ratings_data.take(3)


# In[10]:

small_movies_file = os.path.join(datasets_path, 'ml-latest-small', 'movies.csv')

small_movies_raw_data = sc.textFile(small_movies_file)
small_movies_raw_data_header = small_movies_raw_data.take(1)[0]

small_ratings_data = small_ratings_raw_data.filter(lambda line: line!=small_ratings_raw_data_header)    .map(lambda line: line.split(",")).map(lambda tokens: (int(tokens[0]),int(tokens[1]),float(tokens[2]))).cache()

small_movies_data = small_movies_raw_data.filter(lambda line: line!=small_movies_raw_data_header)    .map(lambda line: line.split(",")).map(lambda tokens: (tokens[0],tokens[1],tokens[2])).cache()
small_movies_titles = small_movies_data.map(lambda x: (int(x[0]),x[1]))
small_movies_genres = small_movies_data.map(lambda x: (int(x[0]),x[2]))
small_movies_genres.take(3)


# In[11]:

small_movies_titles.take(3)


# In[12]:

training_RDD, validation_RDD, test_RDD = small_ratings_data.randomSplit([6, 2, 2], seed=0L)
validation_for_predict_RDD = validation_RDD.map(lambda x: (x[0], x[1]))
test_for_predict_RDD = test_RDD.map(lambda x: (x[0], x[1]))


# In[13]:

from pyspark.mllib.recommendation import ALS
import math

seed = 5L
iterations = 10
regularization_parameter = 0.1
ranks = [4, 8, 12]
errors = [0, 0, 0]
err = 0
tolerance = 0.02

min_error = float('inf')
best_rank = -1
best_iteration = -1
for rank in ranks:
    model = ALS.train(training_RDD, rank, seed=seed, iterations=iterations,
                      lambda_=regularization_parameter)
    predictions = model.predictAll(validation_for_predict_RDD).map(lambda r: ((r[0], r[1]), r[2]))
    rates_and_preds = validation_RDD.map(lambda r: ((int(r[0]), int(r[1])), float(r[2]))).join(predictions)
    error = math.sqrt(rates_and_preds.map(lambda r: (r[1][0] - r[1][1])**2).mean())
    errors[err] = error
    err += 1
    print 'For rank %s the RMSE is %s' % (rank, error)
    if error < min_error:
        min_error = error
        best_rank = rank

print 'The best model was trained with rank %s' % best_rank


# In[14]:

predictions.take(3)


# In[15]:

rates_and_preds.take(3)


# In[16]:

model = ALS.train(training_RDD, best_rank, seed=seed, iterations=iterations,
                      lambda_=regularization_parameter)
predictions = model.predictAll(test_for_predict_RDD).map(lambda r: ((r[0], r[1]), r[2]))
rates_and_preds = test_RDD.map(lambda r: ((int(r[0]), int(r[1])), float(r[2]))).join(predictions)
error = math.sqrt(rates_and_preds.map(lambda r: (r[1][0] - r[1][1])**2).mean())
    
print 'For testing data the RMSE is %s' % (error)


# In[17]:

def get_counts_and_averages(ID_and_ratings_tuple):
    nratings = len(ID_and_ratings_tuple[1])
    return ID_and_ratings_tuple[0], (nratings, float(sum(x for x in ID_and_ratings_tuple[1]))/nratings)

movie_ID_with_ratings_RDD = (small_ratings_data.map(lambda x: (x[1], x[2])).groupByKey())
movie_ID_with_avg_ratings_RDD = movie_ID_with_ratings_RDD.map(get_counts_and_averages)
movie_rating_counts_RDD = movie_ID_with_avg_ratings_RDD.map(lambda x: (x[0], x[1][0]))


# In[18]:

new_user_ID = 0

# The format of each line is (userID, movieID, rating)
new_user_ratings = [
     (0,260,9), # Star Wars (1977)
     (0,1,8), # Toy Story (1995)
     (0,16,7), # Casino (1995)
     (0,25,8), # Leaving Las Vegas (1995)
     (0,32,9), # Twelve Monkeys (a.k.a. 12 Monkeys) (1995)
     (0,335,4), # Flintstones, The (1994)
     (0,379,3), # Timecop (1994)
     (0,296,7), # Pulp Fiction (1994)
     (0,858,10) , # Godfather, The (1972)
     (0,50,8) # Usual Suspects, The (1995)
    ]
new_user_ratings_RDD = sc.parallelize(new_user_ratings)
print 'New user ratings: %s' % new_user_ratings_RDD.take(10)


# In[19]:

small_data_with_new_ratings_RDD = small_ratings_data.union(new_user_ratings_RDD)


# In[20]:


from time import time

t0 = time()
new_ratings_model = ALS.train(small_data_with_new_ratings_RDD, best_rank, seed=seed, 
                              iterations=iterations, lambda_=regularization_parameter)
tt = time() - t0

print "New model trained in %s seconds" % round(tt,3)


# In[21]:

new_user_ratings_ids = map(lambda x: x[1], new_user_ratings) # get just movie IDs
# keep just those not on the ID list (thanks Lei Li for spotting the error!)
new_user_unrated_movies_RDD = (small_movies_data.filter(lambda x: x[0] not in new_user_ratings_ids).map(lambda x: (new_user_ID, x[0])))

# Use the input RDD, new_user_unrated_movies_RDD, with new_ratings_model.predictAll() to predict new ratings for the movies
new_user_recommendations_RDD = new_ratings_model.predictAll(new_user_unrated_movies_RDD)


# In[22]:

# Transform new_user_recommendations_RDD into pairs of the form (Movie ID, Predicted Rating)
new_user_recommendations_rating_RDD = new_user_recommendations_RDD.map(lambda x: (x.product, x.rating))
new_user_recommendations_rating_title_and_count_RDD =     new_user_recommendations_rating_RDD.join(small_movies_titles).join(small_movies_genres).join(movie_rating_counts_RDD)
new_user_recommendations_rating_title_and_count_RDD.take(3)


# In[23]:

new_user_recommendations_rating_title_and_count_RDD =    new_user_recommendations_rating_title_and_count_RDD.map(lambda r: (r[1][0][0][1], r[1][0][0][0], r[1][0][1], r[1][1]))
new_user_recommendations_rating_title_and_count_RDD.take(2)


# In[25]:


top_movies = new_user_recommendations_rating_title_and_count_RDD.filter(lambda r: r[2]>=25).takeOrdered(25, key=lambda x: -x[1])

print ('TOP recommended movies (with more than 25 reviews):\n%s' %
        '\n'.join(map(str, top_movies)))

