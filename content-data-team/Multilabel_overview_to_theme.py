import os
'''
find path of data file I need
'''

current_file_path = __file__
upper_dir = os.path.dirname(os.getcwd())

data_dir = os.path.join(upper_dir, 'data')
fileAllData = os.path.join(data_dir, 'Allmovie_2.csv')
fileTheme = os.path.join(data_dir, 'overview_theme.csv')


'''
  Write overview, which is movie description, and themes to a new CSV file
'''
import csv
f = open(fileAllData,'rb')
reader = csv.DictReader(f)
result = open(fileTheme,'w')
fieldnames = ['movie description','movie theme']
writer = csv.DictWriter(result, fieldnames=fieldnames)
writer.writeheader()
for row in reader:
    newline = row['overview'].lower()
    newkey = row['themes'].lower()
    newres = ''
    for newchar in newkey:
        if newchar.isdigit() or newchar.isalpha() or newchar == ' ' or newchar == ',':
            newres = newres + newchar
    newres = newres.split(',')
    new = ''
    for char in newline:
        if char.isdigit() or char.isalpha() or char == ' ':
            new = new + char
    writer.writerow({'movie description': new, 'movie theme': newres})


'''
  Use tf-idf to represent training data, the training data is the description of each movie
'''
##get training data represenation
import numpy as np
import pandas as pd
from scipy import sparse
df = pd.read_csv('/data/Allmovie_2.csv',header = 0)
X = df['overview'].to_dict()
traindata = []
for idx in xrange(len(X)):
    if str(X[idx]) == 'nan':
        continue
    traindata.append(X[idx])
len(traindata)


##tf-idf data representation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_features = 500)
X = vectorizer.fit_transform(traindata)
print X.shape


'''
  Use sparse matrix to represent label, then use 
'''
##deal with label matrix
#generate unique key for each label
import string
import random
unique = set()
def id_generator(size=3, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))
while len(unique) <= 410:
    unique.add(id_generator())
unique = list(unique)

## create a dictionary for label
import csv
f = open('/data/overview_theme.csv','rb')
reader = csv.DictReader(f)
for row in reader:
    tempt = row['movie theme'].replace("'",'').replace('[','').replace(']','').split(',')
    for item in tempt:
        item = item.strip()
        A.add(item)
res = list(A)[1:]
dictionary = {}
i = 0
for item in res:
    dictionary[item] = unique[i]
    i = i + 1
dictionary[''] = ''
#print dictionary

##for each description, the theme
f2 = open('/data/overview_theme.csv','rb')
reader = csv.DictReader(f2)
result = []
for row in reader:
    temp = []
    tempt = row['movie theme'].replace("'",'').replace('[','').replace(']','').strip().split(',')
    for item in tempt:
        item = item.strip()        
        temp.append(dictionary[item])
    result.append(temp)

#print result

'''
  Use sklearn package to do One-vs-All, the linear_model we use is LogisticRegression
'''
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier

##the sparse matrix for label
from sklearn.preprocessing import MultiLabelBinarizer
y = result
label = MultiLabelBinarizer().fit_transform(y)
X_test = traindata[4001:]
classifier = Pipeline([
    ('vectorizer', TfidfVectorizer(max_features = 1000)),
    ('tfidf', TfidfTransformer()),
    ('clf', OneVsRestClassifier(LogisticRegression()))])
classifier.fit(traindata[:4000], label[:4000])
predicted = classifier.predict(traindata[4001:])
#for item, labels in zip(X_test, predicted):
#    print '%s => %s' % (item, ', '.join(target_names[x] for x in labels))
