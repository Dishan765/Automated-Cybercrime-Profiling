from Preprocessing import Preprocess
from DataAnalysis import  DataAnalysis


def main():
    # Preprocess -> return a dataframe
    # Features -> pass "preprocessed_comments" 
        # use columns "preprocessed_comments" to extract features
        # return a list/array of feature vectors
    # Training
        # Train_Test split -> RETURN TRAIN SET AND TEST SET
            # Pass processed_features and labels as a list
        # LogisticRegression -> pass training set features and labels as 2 list
            # return text_classifier.fit(X_train,y_train)
    # Evaluation
    # use text_classifier.fit(X_train,y_train) as predictions
    # constructor parameters ->x_test and y_test and predictions
    #Save model
    pass
    

if __name__ == "__main__":
    main()