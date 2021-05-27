from numpy.lib.npyio import savez_compressed
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import RandomOverSampler
#from imblearn.pipeline import Pipeline
from collections import Counter
import numpy as np
from sklearn.ensemble import RandomForestClassifier



class TrainTest():
    def __init__(self,features_list,labels):
        self.features_list = features_list
        self.labels = labels

    # Split data into training and testing
    def TrainTestSplit(self):
        X_train, X_test, y_train, y_test = train_test_split(self.features_list, self.labels, test_size=0.3, random_state=42)
        # Make dataset balanced by oversampling
        X_sm_train, y_sm_train = self.overSampling(X_train,y_train)
        print('Original dataset shape {}'.format(Counter(y_train)))
        print('Resampled dataset shape {}'.format(Counter(y_sm_train)))
        
        X_sm_train = X_sm_train.ravel()

        return X_sm_train, X_test, y_sm_train, y_test
        #return X_train, X_test, y_train, y_test

    def overSampling(self,X_train,y_train):
        over =  RandomOverSampler()
        X_train = X_train.reshape(-1,1)
        return over.fit_resample(X_train,y_train)

    # Logistic Regression Model
    def LogisticRegressionModel(self,X_train,y_train):
        # define the stages of the pipeline
        model = LogisticRegression(C=100,max_iter=300)
        #C=10
        tfidf = TfidfVectorizer(use_idf=True, max_features=2500, min_df=7, max_df=0.8)
        #pipeline = Pipeline(steps= [('tfidf', TfidfVectorizer(use_idf=True, max_features=2500, min_df=7, max_df=0.8)), ('model', LogisticRegression())])
        pipeline = Pipeline(steps= [('tfidf', tfidf), ('model', model)])
        # fit the pipeline model with the training data                            
        LR = pipeline.fit(X_train,y_train)

        #Train model
        # LR = LogisticRegression(random_state=0, solver='lbfgs', multi_class='ovr').fit(X_train, y_train)
        # LR = LR.fit(X_train, y_train)

        return LR

    # SVM Model
    def svmModel(self,X_train,y_train):
        np.random.seed(0)
        # define the stages of the pipeline
        #pipeline = Pipeline(steps= [('tfidf', TfidfVectorizer(use_idf=True, max_features=2500, min_df=7, max_df=0.8)), ('model', svm.SVC())])
        model = SVC(kernel='linear',gamma='scale',C=1)
        #kernel='linear',gamma='scale',C=1,class_weight={0:1}
        tfidf = TfidfVectorizer(use_idf=True, max_features=2500, min_df=7, max_df=0.8)
        pipeline = Pipeline(steps= [('tfidf', tfidf), ('model', model)])

        # fit the pipeline model with the training data                            
        SVM = pipeline.fit(X_train,y_train)

        #Train model
        # SVM = svm.LinearSVC()
        # SVM = SVM.fit(X_train, y_train)

        return SVM

    # Decision Tree Model
    def dtModel(self,X_train,y_train):
        # define the stages of the pipeline
        #pipeline = Pipeline(steps= [('tfidf', TfidfVectorizer(use_idf=True, max_features=2500, min_df=7, max_df=0.8)), ('model', tree.DecisionTreeClassifier())])
        model = DecisionTreeClassifier(splitter='random',max_depth=None,max_features=None,min_samples_leaf=4,min_samples_split=25)
        #splitter='random',max_depth=None,max_features=None,min_samples_leaf=2,min_samples_split=25,class_weight={0:2}
        #{'max_depth': 15, 'max_features': None, 'min_samples_leaf': 4, 'min_samples_split': 15, 'splitter': 'best'}
        tfidf = TfidfVectorizer(use_idf=True, max_features=2500, min_df=7, max_df=0.8)
        pipeline = Pipeline(steps= [('tfidf', tfidf), ('model', model)])
        # fit the pipeline model with the training data                            
        DT = pipeline.fit(X_train,y_train)


        #Train model
        # DT = tree.DecisionTreeClassifier()
        # DT = DT.fit(X_train, y_train)

        return DT

    # Decision Tree Model
    def randomForestModel(self,X_train,y_train):
        # define the stages of the pipeline
        model = RandomForestClassifier(max_depth=2,random_state=0)
        tfidf = TfidfVectorizer(use_idf=True, max_features=2500, min_df=7, max_df=0.8)
        pipeline = Pipeline(steps= [('tfidf', tfidf), ('model', model)])
        # fit the pipeline model with the training data                            
        rf = pipeline.fit(X_train,y_train)


        #Train model
        # DT = tree.DecisionTreeClassifier()
        # DT = DT.fit(X_train, y_train)

        return rf
    
    
    def Eval(self,classifier,X_test, y_test):
        #Test Model
        y_pred = classifier.predict(X_test)
        #Print Evaluation details
        print(confusion_matrix(y_test,y_pred))
        print(classification_report(y_test,y_pred))
        print(accuracy_score(y_test, y_pred))

    def saveModel(self,classifier,file_name):
        with open(file_name, 'wb') as picklefile:
            pickle.dump(classifier,picklefile)
        
        return file_name

    def loadModel(self, file_name):
        with open(file_name, 'rb') as training_model:
            model = pickle.load(training_model)
        return model