from extractFeaturesFromIPPairs import extractFeaturesFromIPPairs

if __name__ == "__main__":

    extractFeatures = True
    if extractFeatures:
        pcap_dir = "pcap_dir"
        feature_file = "feature.csv"
        extractFeaturesFromIPPairs(pcap_dir, feature_file)
    else:
        pass

 