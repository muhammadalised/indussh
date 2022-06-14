import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class Recommender:
    products = pd.DataFrame(columns=['id', 'article_no', 'name', 'description', 'category'])
    recommendations = {}

    def __init__(self, products):

        self.products = products

        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
        tfidf_matrix = tf.fit_transform(self.products['details'])
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
        
        for idx, row in self.products.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
            similar_items = [(cosine_similarities[idx][i], self.products['article_no'][i]) for i in similar_indices]

            # First item is the item itself, so remove it.
            # Each dictionary entry is like: [(1,2), (3,4)], with each tuple being (score, item_id)
            self.recommendations[row['article_no']] = similar_items[1:]


    # Function to get a friendly item name from the description field, given an item ID
    def item(self, article_no):
        return self.products.loc[self.products['article_no'] == article_no]['description'].tolist()[0].split(' - ')[0]

    # Reads the results out of the dictionary. No real logic here.
    def recommend(self, item_article_no, num):
        recs = self.recommendations[item_article_no]
        recs = sorted(recs, key=lambda tup: tup[0], reverse=True) # Sort the recommendations based on their score in descending order
        return recs[:num]

