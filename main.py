from FeatureExtractor import FeatureExtractor
from FeatureExtractorWitfhDistance import FeatureExtractorWitfhDistance
from Classifier import Classifier
from ForestClassifier import ForestClassifier

if __name__ == "__main__":

    extractFeatures = False
    if extractFeatures:
        featureExtractor = FeatureExtractor('pcap_dir/file_and_cmd_pcap', 'feature_csv_file/file_and_cmd_features.csv')
        # featureExtractor = FeatureExtractorWitfhDistance('pcap_dir/file_and_cmd_pcap', 'feature_csv_file/file_and_cmd_features.csv')
        featureExtractor.extractFeaturesFromIPPairs()

    else:
        classifier = Classifier()
        # classifier = ForestClassifier()
        classifier.classifier('feature_csv_file/file_and_cmd_features.csv')
