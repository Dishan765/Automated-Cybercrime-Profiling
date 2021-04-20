from Preprocessing import Preprocess
from DataAnalysis import  DataAnalysis
from Features import FeatureExtraction
from Training import TrainTest
import pickle

def main():
    #  PRE-PROCESSING
    dataset_name = "GenerateDataset/SmallDatasets/smallDataset.csv"
    processed_dataset = "GenerateDataset/SmallDatasets/processSmallDataset.csv"
    process = Preprocess(dataset_name,processed_dataset)
    # Preprocess -> return processed comment in a dataframe
    processedDF = process.preprocess()

    # ANALYSE PRE-PROCESSED COMMENTS
    print(processedDF.head(10))
    analyse = DataAnalysis(processed_dataset,"processed_comments")
    analyse.generalInfo()
    analyse.pie_chart()
    analyse.label_barchart()

    # # STORE PROCESSED FEATURES IN A LIST
    processedFeatures = processedDF.iloc[:,4].values
    # labels = processedDF.iloc[:,3].values
    # # print(processedFeatures)
    # # print(labels)

    # # FEATURE EXTRACTION - obsolete since using pipeline
    # # Features -> pass "preprocessed_comments" 
    # #feature = FeatureExtraction(processedFeatures)
    # # list/array of feature vectors
    # #feature_vectors = feature.tf_idf()
    # #feature_vectors = processedFeatures
    # #print(len(processedFeatures))

    # # TRAIN_TEST SPLIT
    train = TrainTest(processedFeatures,labels)
    X_train, X_test, y_train, y_test = train.TrainTestSplit()
    # #print(X_test[0])

    # #TRAINING USING LR
    print("\tLogistic Regression:")
    LR = train.LogisticRegressionModel(X_train,y_train,X_test)
    train.Eval(LR,X_test, y_test)
    print(LR.predict(["To fou"]))
    #Save model
    train.saveModel(LR,"./Models/LRclassifier.pkl")
    
    # #TRAINING USING SVM
    print("\tSVM:")
    svm = train.svmModel(X_train,y_train,X_test)
    train.Eval(svm,X_test, y_test)
    print(svm.predict(["To fou"]))
    #Save model
    train.saveModel(svm,"./Models/SVMclassifier.pkl")

    # # TRAINING USING DECISION TREE
    print("\tDecision Tree:")
    dt = train.dtModel(X_train,y_train,X_test)
    train.Eval(dt,X_test, y_test)
    print(dt.predict(["To fou"]))
    #Save model
    train.saveModel(dt,"./Models/DTclassifier.pkl")
    
    # Loading model to compare the results
    LR = train.loadModel('./Models/LRclassifier.pkl')
    print(LR.predict(["To fou"]))
    svm = train.loadModel('./Models/SVMclassifier.pkl')
    print(svm.predict(["To fou"]))
    dt = train.loadModel('./Models/SVMclassifier.pkl')
    print(dt.predict(["To fou"]))

    


if __name__ == "__main__":
    main()