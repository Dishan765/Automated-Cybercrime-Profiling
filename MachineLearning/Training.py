from Features import FeatureExtraction

class Training():
    
    def __init__(self,dataset_name):
        self.process = FeatureExtraction(dataset_name)


    # return array of TF-IDF feature vectors
    def tf_idf():
        pass

# Split data into training and testing
# Return test and train set only