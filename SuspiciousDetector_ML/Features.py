from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# OBSOLETE since using pipeline
class FeatureExtraction():
    
    def __init__(self,feature_list):
        self.feature_list = feature_list
    

    # return array of TF-IDF feature vectors
    def tf_idf(self):
        stop_words = ['la', 'le', 'mo', 'pa', 'so', 'ti', 'de', 'fer', 'si',
            'ou', 'pe', 'ek', 'enn', 'sa', 'zot', 'dan', 'pou', 'a', 'b', 'li']
        #use feature_list to extract vectors
        vectorizer = TfidfVectorizer(use_idf=True,max_features=5000, min_df=7, max_df=0.8)
        tfIdf = vectorizer.fit_transform(self.feature_list)
        df = pd.DataFrame(tfIdf[0].T.todense(), index=vectorizer.get_feature_names(), columns=["TF-IDF"])
        df = df.sort_values('TF-IDF', ascending=False)
        print (df.head(25))


df = pd.read_csv("GenerateDataset/Datasets/processedDataset2.csv")
t = FeatureExtraction(df["processed_comments"])
print(t.tf_idf())