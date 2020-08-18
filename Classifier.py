import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_curve
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
import os
from sklearn.tree import export_graphviz

# Where to save the figures
PROJECT_ROOT_DIR = "."
CHAPTER_ID = "classification"
IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "images", CHAPTER_ID)
os.makedirs(IMAGES_PATH, exist_ok=True)


def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


def plot_roc_curve(fpr, tpr, label=None):
    plt.plot(fpr, tpr, linewidth=2, label=label)
    plt.plot([0, 1], [0, 1], 'k--')  # Dashed diagonal
    plt.xlabel('False Positive Rate (Fall-Out)', fontsize=16)  # Not shown
    plt.ylabel('True Positive Rate (Recall)', fontsize=16)  # Not shown
    plt.grid(True)


def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
    plt.plot(thresholds, precisions[:-1], "b--", label="Precision")
    plt.plot(thresholds, recalls[:-1], "g-", label="Recall")
    plt.legend(loc="lower right", fontsize=16)  # Not shown in the book
    plt.xlabel("Threshold", fontsize=16)  # Not shown
    plt.grid(True)


def plot_precision_vs_recall(precisions, recalls):
    plt.plot(recalls, precisions, "b-", linewidth=2)
    plt.xlabel("Recall", fontsize=16)
    plt.ylabel("Precision", fontsize=16)
    plt.axis([0, 1, 0, 1])
    plt.grid(True)


def classifier(feature_csv_file):

    features = pd.read_csv(feature_csv_file)
    # train_set, test_set = train_test_split(features, test_size=0.4,random_state=42)
    train_set = features
    train_features = train_set.drop("label", axis=1)
    train_labels = train_set["label"].copy()
    # scaler = StandardScaler()
    # train_features_scaled = scaler.fit_transform(
    #     train_features.astype(np.float64))
    # train_features = train_features_scaled
    clf = tree.DecisionTreeClassifier(criterion='entropy')
    clf = clf.fit(train_features, train_labels)

    export_graphviz(clf,
                    out_file=os.path.join(IMAGES_PATH, "iris_tree.dot"),
                    feature_names=features.columns[:-1],
                    class_names=["NoICMPTunnel", "hasICMPTunnel"],
                    rounded=True,
                    filled=True)

    y_train_pred = cross_val_predict(clf, train_features, train_labels, cv=10)
    print("pred=" + str(y_train_pred))
    matrix = confusion_matrix(train_labels, y_train_pred)
    print('confusion_matrix:')
    print(matrix)
    precision = precision_score(train_labels, y_train_pred)
    recall = recall_score(train_labels, y_train_pred)
    f1 = f1_score(train_labels, y_train_pred)

    print('precision=' + str(precision))
    print('recall=' + str(recall))
    print('f1_score=' + str(f1))

    y_probas_tree = cross_val_predict(clf,
                                      train_features,
                                      train_labels,
                                      cv=10,
                                      method="predict_proba")
    # print(y_probas_tree)
    y_scores_tree = y_probas_tree[:, 1]  # score = proba of positive class
    print('y_scores_tree=' + str(y_scores_tree))
    # y_scores = cross_val_predict(clf, train_features, train_labels, cv=10,method="decision_function")
    precisions, recalls, thresholds = precision_recall_curve(
        train_labels, y_scores_tree)
    print('precisions:' + str(precisions), 'recalls:' + str(recalls),
          'thresholds:' + str(thresholds))

    threshold_90_precision = thresholds[np.argmax(precisions >= 0.90)]
    y_train_pred_90 = (y_scores_tree >= threshold_90_precision)
    precision_score_90 = precision_score(train_labels, y_train_pred_90)
    recall_score_90 = recall_score(train_labels, y_train_pred_90)
    print('y_train_pred_90' + str(y_train_pred_90))
    print('precision_score_90=' + str(precision_score_90))
    print('recall_score_90=' + str(recall_score_90))

    plot_precision_recall_vs_threshold(precisions, recalls, thresholds)
    plt.plot([0.673364, 0.673364], [0, 0.83822], 'r:')
    plt.plot([0, 0.673364], [0.83822, 0.83822], 'r:')
    plt.plot([0.673364], [0.83822], 'ro')
    save_fig("precision_recall_vs_threshold_plot")
    plt.show()

    plt.figure(figsize=(8, 6))
    plot_precision_vs_recall(precisions, recalls)
    plt.plot([0.748487, 0.748487], [0, 1], 'r:')
    plt.plot([0, 0.748487], [1, 1], 'r:')
    plt.plot([0.748487], [1], 'ro')
    save_fig("plot_precision_vs_recall")
    plt.show()

    fpr, tpr, thresholds = roc_curve(train_labels, y_scores_tree)
    roc_auc = roc_auc_score(train_labels, y_scores_tree)
    print("roc_auc: " + str(roc_auc))
    plot_roc_curve(fpr, tpr)
    plt.plot([0, 0], [0, 0.757218], 'r:')
    plt.plot([0, 0], [0.757218, 0.757218], 'r:')
    plt.plot([0], [0.757218], 'ro')
    save_fig("plot_roc_curve")
    plt.show()
