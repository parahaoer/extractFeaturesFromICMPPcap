from FeatureExtractor import FeatureExtractor 
from Classifier import classifier

if __name__ == "__main__":

    extractFeatures = True
    if extractFeatures:

        featureExtractor = FeatureExtractor()
        featureExtractor.extractFeaturesFromIPPairs()

    else:
        classifier('feature.csv')

 