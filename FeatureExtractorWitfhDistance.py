from FeatureExtractor import FeatureExtractor
'''
    多进程的缺点： 当其中一个子进程中出错时可能不会报错，直接被跳过，就需要改成单进程来排错。
    而且，debug进入不了子进程的函数。
'''


class FeatureExtractorWitfhDistance(FeatureExtractor):

    def extractFeaturesWithMultiprocess(self, ip_pair_datas, features,
                                        is_positive_sample):

        feature_from_distance = super().extractDistanceFeature(ip_pair_datas)

        feature_vec = feature_from_distance

        if is_positive_sample is True:
            feature_vec.append(1)
        elif is_positive_sample is False:
            feature_vec.append(0)
        features.append(feature_vec)

    def create_csv_header(self):
        # 3. 构建列表头
        header_list = []

        auxiliary_list1 = [
            "distance_in_ICMP_pair_percentile",
            "distance_between_type_8_percentile",
            "distance_between_type_0_percentile"
        ]
        aux_list2 = ["0", "25", "50", "75", "100", "mean"]
        for item1 in auxiliary_list1:
            for item2 in aux_list2:
                if item2 == "mean":
                    header = item1[:-10] + item2
                else:
                    header = item1 + '_' + item2
                header_list.append(header)
        header_list.append("label")

        return header_list
