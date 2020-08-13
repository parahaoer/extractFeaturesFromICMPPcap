from extractFeaturesFromIPPairs import extractFeaturesFromIPPairs
from Classifier import classifier

if __name__ == "__main__":

    extractFeatures = True
    if extractFeatures:
        is_negative_sample = False
        pcap_dir = "pcap_dir/positive-icmp"
        feature_file = "positive_feature.csv"
        extractFeaturesFromIPPairs(pcap_dir, feature_file, is_negative_sample)
    else:
        classifier('feature.csv')

 