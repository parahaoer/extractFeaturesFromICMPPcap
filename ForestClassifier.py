from Classifier import Classifier
from sklearn.ensemble import RandomForestClassifier


class ForestClassifier(Classifier):
    def __init__(self):
        save_path = "Forest"
        self.make_pic_path(save_path)

    def classifier(self, feature_csv_file):
        train_features, train_labels, _ = self.getTrainSet(feature_csv_file)
        # scaler = StandardScaler()
        # train_features_scaled = scaler.fit_transform(
        #     train_features.astype(np.float64))
        # train_features = train_features_scaled
        forest_clf = RandomForestClassifier()
        clf = forest_clf.fit(train_features, train_labels)

        self.evalClassifier(clf, train_features, train_labels)
