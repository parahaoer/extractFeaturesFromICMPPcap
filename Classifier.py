import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

def plot_roc_curve(fpr, tpr, label=None):
    plt.plot(fpr, tpr, linewidth=2, label=label)
    plt.plot([0, 1], [0, 1], 'k--') # Dashed diagonal
    [...] # Add axis labels and grid


def classifier(feature_csv_file):

    features = pd.read_csv(feature_csv_file)
    # train_set, test_set = train_test_split(features, test_size=0.4,random_state=42)
    train_set = features
    train_features = train_set.drop("label", axis=1)
    train_labels = train_set["label"].copy()
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(train_features, train_labels)
    y_train_pred = cross_val_predict(clf, train_features, train_labels, cv=3)
    matrix = confusion_matrix(train_labels, y_train_pred)
    print(matrix)
    precision = precision_score(train_labels, y_train_pred)
    recall = recall_score(train_labels, y_train_pred) 
    f1 = f1_score(train_labels, y_train_pred)
    fpr, tpr, thresholds = roc_curve(train_labels, y_train_pred)
    print(precision)
    print(recall)
    print(f1)
    plot_roc_curve(fpr, tpr)
    plt.show()

