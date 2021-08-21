from pandas.io.parsers import read_csv
from Preprocessing import Preprocess
from DataAnalysis import DataAnalysis
from Training import TrainTest
import pickle
import pandas as pd
from os import path
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier


def main():
    #  PRE-PROCESSING
    dataset_name = "GenerateDataset/Datasets/Dataset2.csv"
    processed_dataset = "GenerateDataset/Datasets/processedDataset2.csv"

    # If dataset already processed, just read file
    if path.exists(processed_dataset):
        processedDF = pd.read_csv(processed_dataset)
    else:
        # Processed the data set if it is not processed
        process = Preprocess(dataset_name, processed_dataset)
        # Preprocess -> return processed comment in a dataframe
        processedDF = process.preprocess()

    # ANALYSE PRE-PROCESSED COMMENTS
    # print(processedDF.head(10))
    # analyse = DataAnalysis(processed_dataset, "processed_comments")
    # analyse.generalInfo()
    # # Barchart - labels count for training data set
    # analyse.barchart_labels()
    # analyse.pie_chart()
    # analyse.barchart_labels_per_source()

    # STORE PROCESSED FEATURES IN A LIST
    processedFeatures = processedDF.iloc[:, 4].values
    print(len(processedFeatures))
    labels = processedDF.iloc[:, 3].values
    print(len(labels))

    # FEATURE EXTRACTION - obsolete since using pipeline
    # Features -> pass "preprocessed_comments"
    # feature = FeatureExtraction(processedFeatures)
    # # list/array of feature vectors
    # feature_vectors = feature.tf_idf()
    # feature_vectors = processedFeatures
    # # print(len(processedFeatures))

    # # TRAIN_TEST SPLIT
    train = TrainTest(processedFeatures, labels)
    X_train, X_test, y_train, y_test = train.TrainTestSplit()

    # Finding best parameters for SVM,DT,LR
    # LR
    # vectorizer = TfidfVectorizer(use_idf=True, max_features=2500, min_df=7, max_df=0.8)
    # X_train = vectorizer.fit_transform(X_train).toarray()
    # param_grid = {"C": [0.1, 1, 10, 100]}
    # grid = GridSearchCV(LogisticRegression(max_iter=200), param_grid, refit=True, verbose=3, n_jobs=-1)
    # # fitting the model for grid search
    
    # grid.fit(X_train, y_train)

    # ## print best parameter after tuning
    # print(grid.best_params_)

    # #SVM
    # vectorizer = TfidfVectorizer(use_idf=True, max_features=2500, min_df=7, max_df=0.8)
    # X_train = vectorizer.fit_transform(X_train).toarray()
    # param_grid = {'C': [0.1, 1, 10, 100],  
    #           'gamma': [1, 0.1, 0.01, 0.001, 0.0001], 
    #           'gamma':['scale', 'auto'],
    #           'kernel': ['linear']
    #           }
    # grid = GridSearchCV(SVC(), param_grid, refit=True, verbose=3, n_jobs=-1)
    # # fitting the model for grid search
    # grid.fit(X_train, y_train)
    # print(grid.best_params_)
    
    #DT
    # vectorizer = TfidfVectorizer(use_idf=True, max_features=2500, min_df=7, max_df=0.8)
    # X_train = vectorizer.fit_transform(X_train).toarray()
    # param_grid = {'min_samples_split': [2, 4, 6, 10, 15, 25],
    #                   'min_samples_leaf': [1, 2, 4, 10],
    #                   'max_depth': [None, 4, 10, 15],
    #                   'splitter' : ('best', 'random'),
    #                   'max_features':[None, 2, 4, 6, 8, 10, 12, 14]
    #                   }
    


    # grid = GridSearchCV(DecisionTreeClassifier(), param_grid, refit=True, verbose=3, n_jobs=-1)
    # # fitting the model for grid search
    
    # grid.fit(X_train, y_train)

    ## print best parameter after tuning
    #print(grid.best_params_)

    # TRAINING USING LR
    print(
        "***********************************************************************************************************"
    )
    print("\tLogistic Regression:")
    LR = train.LogisticRegressionModel(X_train, y_train)
    # Evaluate trained model
    train.Eval(LR, X_test, y_test)
    # Save model
    train.saveModel(LR, "./Models/LRclassifier.pkl")

    # # #TRAINING USING SVM
    print(
        "***********************************************************************************************************"
    )
    print("\tSVM:")
    svm = train.svmModel(X_train, y_train)
    # Evaluate trained model
    train.Eval(svm, X_test, y_test)
    # Save model
    train.saveModel(svm, "./Models/SVMclassifier.pkl")

    # # TRAINING USING DECISION TREE
    print(
        "***********************************************************************************************************"
    )
    print("\tDecision Tree:")
    dt = train.dtModel(X_train, y_train)
    # Evaluate trained model
    train.Eval(dt, X_test, y_test)
    # Save model
    train.saveModel(dt, "./Models/DTclassifier.pkl")

    # Loading model to compare the results
    LR = train.loadModel("./Models/LRclassifier.pkl")
    print(LR.predict(["BLD"]))
    svm = train.loadModel("./Models/SVMclassifier.pkl")
    print(svm.predict(["BLD"]))
    dt = train.loadModel("./Models/SVMclassifier.pkl")
    print(dt.predict(["Ale mort"]))
    # rf = train.loadModel("./Models/RFclassifier.pkl")
    # print(rf.predict(["Ale suicider"]))

if __name__ == "__main__":
    main()
