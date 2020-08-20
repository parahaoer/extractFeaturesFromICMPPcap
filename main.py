from FeatureExtractor import FeatureExtractor
from FeatureExtractorWitfhDistance import FeatureExtractorWitfhDistance
from Classifier import Classifier
from ForestClassifier import ForestClassifier

if __name__ == "__main__":

    extractFeatures = False
    if extractFeatures:
        # featureExtractor = FeatureExtractor()
        featureExtractor = FeatureExtractorWitfhDistance()
        featureExtractor.extractFeaturesFromIPPairs()

    else:
        # classifier = Classifier()
        classifier = ForestClassifier()
        classifier.classifier('distance_feature.csv')
