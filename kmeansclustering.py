
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

file = open("Clusters.txt", "w")
tweets_read_in = pd.read_csv("/Users/eveohagan/brexit.csv")


# Extracting usernames / hastag / text  from tweets
tweets_username = tweets_read_in['username']
tweets_hashtags = tweets_read_in['hashtags']
tweets_text = tweets_read_in['text']

vectorizer = TfidfVectorizer(stop_words='english')

# Vectorising the usernames / hashtag / text 
username = vectorizer.fit_transform(tweets_username)
hashtags = vectorizer.fit_transform(tweets_hashtags)
text = vectorizer.fit_transform(tweets_text)
k = 8

# Username clustering
model_usernames = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
model_usernames.fit(username)

# Print top 10 usernames per cluster
print("Top usernames per cluster:")
file.write("Top usernames per cluster:\n")
centroids = model_usernames.cluster_centers_.argsort()[:, ::-1]
terms_username = vectorizer.get_feature_names()
for i in range(k):
    print ("Cluster %d:" % i)
    file.write("Cluster %d:" % i)
    file.write("\n")
    for ind in centroids[i, :10]:
        print (' %s' % terms_username[ind])
        file.write(' %s' % terms_username[ind])
        file.write("\n")

#print("\n")
open("Clusters.txt", "w+")

# Hashtag clustering
model_hashtags = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
model_hashtags.fit(hashtags)

# Print top 10 hashtags per cluster
print("Top hashtags per cluster:")
file.write("\nTop hashtags per cluster:\n")
centroids = model_hashtags.cluster_centers_.argsort()[:, ::-1]
terms_hashtags = vectorizer.get_feature_names()
for i in range(k):
    print ("Cluster %d:" % i)
    file.write("Cluster %d:" % i)
    file.write("\n")
    for ind in centroids[i, :10]:
        print (' %s' % terms_hashtags[ind])
        file.write(' %s' % terms_hashtags[ind])
        file.write("\n")

print("\n")

# Text clustering 
model_text = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
model_text.fit(text)

# Print top 10 text per cluster
print("Top text per cluster:")
file.write("\nTop text per cluster:\n")
centroids = model_text.cluster_centers_.argsort()[:, ::-1]
terms_text = vectorizer.get_feature_names()
for i in range(k):
    print ("Cluster %d:" % i)
    file.write("Cluster %d:" % i)
    file.write("\n")
    for ind in centroids[i, :10]:
        print (' %s' % terms_text[ind])
        file.write(' %s' % terms_text[ind])
        file.write("\n")

file.close()
# https://stackoverflow.com/questions/27889873/clustering-text-documents-using-scikit-learn-kmeans-in-python?fbclid=IwAR13agTGUdH3e7Xdpt2x6ee6R8vrzjWCuguWgCgTklOcmcYBwVdO6ak8c3k