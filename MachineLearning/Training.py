from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

class TrainTest():
    
    def __init__(self,features_vectors,labels):
        self.features_vectors = features_vectors
        self.labels = labels

    # Split data into training and testing
    def TrainTestSplit(self):
        X_train, X_test, y_train, y_test = train_test_split(self.features_vectors, self.labels, test_size=0.2, random_state=0)
        return X_train, X_test, y_train, y_test

    # Logistic Regression Model
    def LogisticRegressionModel(self,X_train,y_train,X_test):
        #Train model
        LR = LogisticRegression(random_state=0, solver='lbfgs', multi_class='ovr').fit(X_train, y_train)
        LR.fit(X_train, y_train)

        #Test model
        y_pred = LR.predict(X_test)

        # Save Model and return the saved model path
        # with open('LR_classifier', 'wb') as picklefile:
        #     pickle.dump(classifier,picklefile)
        return y_pred

    # SVM Model
    def svmModel(self,X_train,y_train,X_test):
        #Train model
        SVM = svm.LinearSVC()
        SVM.fit(X_train, y_train)

        #Test model
        y_pred = SVM.predict(X_test)

        # Save Model and return the saved model path
        # with open('LR_classifier', 'wb') as picklefile:
        #     pickle.dump(classifier,picklefile)
        return y_pred

    # SVM Model
    def svmModel(self,X_train,y_train,X_test):
        #Train model
        SVM = svm.LinearSVC()
        SVM.fit(X_train, y_train)

        #Test model
        y_pred = SVM.predict(X_test)

        # Save Model and return the saved model path
        # with open('LR_classifier', 'wb') as picklefile:
        #     pickle.dump(classifier,picklefile)
        return y_pred
    
    
    def Eval(self,y_test,y_pred):        
        print(confusion_matrix(y_test,y_pred))
        print(classification_report(y_test,y_pred))
        print(accuracy_score(y_test, y_pred))

