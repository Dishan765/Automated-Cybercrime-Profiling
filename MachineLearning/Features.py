from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

class FeatureExtraction():
    
    def __init__(self,feature_list):
        self.feature_list = feature_list

    # return array of TF-IDF feature vectors
    def tf_idf(self):
        #use feature_list to extract vectors
        vectorizer = TfidfVectorizer(use_idf=True, max_features=2500, min_df=7, max_df=0.8)
        return vectorizer.fit_transform(self.feature_list).toarray()

#df = pd.read_csv("GenerateDataset/SmallDatasets/processSmallDataset.csv")
#t = FeatureExtraction(df["processed_comments"])
#print(t.tf_idf())