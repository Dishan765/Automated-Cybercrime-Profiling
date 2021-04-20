from numpy.lib.npyio import savez_compressed
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import svm, tree
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer


class TrainTest():
    
    def __init__(self,features_list,labels):
        self.features_list = features_list
        self.labels = labels

    # Split data into training and testing
    def TrainTestSplit(self):
        X_train, X_test, y_train, y_test = train_test_split(self.features_list, self.labels, test_size=0.2, random_state=0)
        return X_train, X_test, y_train, y_test

    # Logistic Regression Model
    def LogisticRegressionModel(self,X_train,y_train,X_test):
        # define the stages of the pipeline
        pipeline = Pipeline(steps= [('tfidf', TfidfVectorizer(use_idf=True, max_features=2500, min_df=7, max_df=0.8)), ('model', LogisticRegression())])
        # fit the pipeline model with the training data                            
        LR = pipeline.fit(X_train,y_train)

        #Train model
        # LR = LogisticRegression(random_state=0, solver='lbfgs', multi_class='ovr').fit(X_train, y_train)
        # LR = LR.fit(X_train, y_train)

        return LR

    # SVM Model
    def svmModel(self,X_train,y_train,X_test):
        # define the stages of the pipeline
        pipeline = Pipeline(steps= [('tfidf', TfidfVectorizer(use_idf=True, max_features=2500, min_df=7, max_df=0.8)), ('model', svm.SVC())])
        # fit the pipeline model with the training data                            
        SVM = pipeline.fit(X_train,y_train)

        #Train model
        # SVM = svm.LinearSVC()
        # SVM = SVM.fit(X_train, y_train)

        return SVM

    # Decision Tree Model
    def dtModel(self,X_train,y_train,X_test):
        # define the stages of the pipeline
        pipeline = Pipeline(steps= [('tfidf', TfidfVectorizer(use_idf=True, max_features=2500, min_df=7, max_df=0.8)), ('model', tree.DecisionTreeClassifier())])
        # fit the pipeline model with the training data                            
        DT = pipeline.fit(X_train,y_train)


        #Train model
        # DT = tree.DecisionTreeClassifier()
        # DT = DT.fit(X_train, y_train)

        return DT
    
    
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