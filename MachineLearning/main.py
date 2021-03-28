from Preprocessing import Preprocess
from DataAnalysis import  DataAnalysis
from Features import FeatureExtraction
from Training import TrainTest

def main():
    #  PRE-PROCESSING
    dataset_name = "GenerateDataset/SmallDatasets/smallDataset.csv"
    processed_dataset = "GenerateDataset/SmallDatasets/processSmallDataset.csv"
    process = Preprocess(dataset_name,processed_dataset)
    # Preprocess -> return processed comment in a dataframe
    processedDF = process.preprocess()

    # ANALYSE PRE-PROCESSED COMMENTS
    # print(processedDF.head(10))
    # analyse = DataAnalysis(processed_dataset,"processed_comments")
    # analyse.pie_chart()
    # analyse.label_barchart()

    # STORE PROCESSED FEATURES IN A LIST
    processedFeatures = processedDF.iloc[:,4].values
    labels = processedDF.iloc[:,3].values
    # print(processedFeatures)
    # print(labels)

    # FEATURE EXTRACTION
    # Features -> pass "preprocessed_comments" 
    feature = FeatureExtraction(processedFeatures)
    # list/array of feature vectors
    feature_vectors = feature.tf_idf()


    # TRAIN_TEST SPLIT
    train = TrainTest(feature_vectors,labels)
    X_train, X_test, y_train, y_test = train.TrainTestSplit()
    # print(y_test)

    #TRAINING USING LR
    y_pred = train.LogisticRegressionModel(X_train,y_train,X_test)
    train.Eval(y_test,y_pred)

    
    #TRAINING USING SVM
    y_pred = train.svmModel(X_train,y_train,X_test)

    # EVALUATION 
    train.Eval(y_test,y_pred)

    # Evaluation
    # use text_classifier.fit(X_train,y_train) as predictions
    # constructor parameters ->x_test and y_test and predictions
    #Save model
    pass
    

if __name__ == "__main__":
    main()