from math import pi
from sklearn import datasets
from sklearn import neighbors
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
import numpy as np
import os
import pickle

# define a Gaussain NB classifier
#clf = GaussianNB()
classifiers=[GaussianNB(),RandomForestClassifier(n_estimators=200),KNeighborsClassifier(n_neighbors=6,n_jobs=-1),LogisticRegression(max_iter=1000)]
names=['gaussianNB','randomforestclassifier','KNNClassifier','LogisticRegression']



# define the class encodings and reverse encodings
classes = {0: "Iris Setosa", 1: "Iris Versicolour", 2: "Iris Virginica"}
r_classes = {y: x for x, y in classes.items()}

# function to train and load the model during startup
def load_model():
    # load the dataset from the official sklearn datasets
    X, y = datasets.load_iris(return_X_y=True)

    # do the test-train split and train the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model_list=[]
    accuracy=[]
    for clf in classifiers:
        #clf.fit(X_train, y_train)
        clf.fit(X_train,y_train)

        # calculate the print the accuracy score
        acc = accuracy_score(y_test, clf.predict(X_test))
        print(f"Model {clf} trained with accuracy: {round(acc, 3)}")
        accuracy.append(acc)
        model_list.append(clf)
        acc=0

    
    acc_index=np.argmax(accuracy)

    loaded_model=model_list[acc_index]
    print(f"loading {loaded_model} with accuracy {accuracy[acc_index]}")
    pickle.dump(loaded_model,open('model.pkl','wb'))


# function to predict the flower using the model
def predict(query_data):
    clf=pickle.load(open('model.pkl','rb'))
    x = list(query_data.dict().values())
    prediction = clf.predict([x])[0]
    print(f"Model prediction: {classes[prediction]}")
    return classes[prediction]

# function to retrain the model as part of the feedback loop
def retrain(data):
    # pull out the relevant X and y from the FeedbackIn object
    clf=pickle.load(open('model.pkl','rb'))
    X = [list(d.dict().values())[:-1] for d in data]
    y = [r_classes[d.flower_class] for d in data]

    # fit the classifier again based on the new data obtained
    clf.fit(X, y)