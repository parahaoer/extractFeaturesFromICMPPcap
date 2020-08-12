from extractFeaturesFromIPPairs import extractFeaturesFromIPPairs

if __name__ == "__main__":

    extractFeatures = True
    if extractFeatures:
        is_negative_sample = True
        pcap_dir = "negative-icmp"
        feature_file = "negative_feature.csv"
        extractFeaturesFromIPPairs(pcap_dir, feature_file, is_negative_sample)
    else:
        pass

 