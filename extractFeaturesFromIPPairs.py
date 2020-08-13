import numpy as np
from analyzePcap import get_filelist
from getLevenshtein import getDistanceInICMPPair, getDistanceBetweenSameside
from multiprocessing import Pool #多进程
from multiprocessing import Manager, Process
import csv

def extractFeaturesFromPayloadLen(datas):
    packets_amount = len(datas)

    the_src_ip = ""

    is_first_echo_request = True

    type_0_packet_list =[]
    type_8_packet_list = []
    type_3_packet_list = []

    src_ip_packet_list = []

    for data in datas:
        
        ip_packet = data.payload
        icmp_packet = ip_packet.payload

        src_ip = ip_packet.fields['src']
        try:
            icmp_fields = icmp_packet.fields

            icmp_type = icmp_fields['type']

            if icmp_type == 0:
                type_0_packet_list.append(data)
            elif icmp_type == 8:
                type_8_packet_list.append(data)
                if is_first_echo_request:
                    the_src_ip = src_ip
                    
                    is_first_echo_request = False
            elif icmp_type == 3:
                type_3_packet_list.append(data)
            
            if the_src_ip is not "" and the_src_ip == src_ip:
                src_ip_packet_list.append(data)
        except KeyError as e:
            print(ip_packet.fields['src'])
            pass

    
    type_0_packet_per_IPPair =  len(type_0_packet_list) / packets_amount
    type_3_packet_per_IPPair =  len(type_3_packet_list) / packets_amount
    type_8_packet_per_IPPair =  len(type_8_packet_list) / packets_amount
    src_ip_amount = len(src_ip_packet_list)

    type_0_payload_len_list = extractPayloadLenFeature(type_0_packet_list)
    type_8_payload_len_list = extractPayloadLenFeature(type_8_packet_list)

    type_0_payload_len_percentile = getPercentile(type_0_payload_len_list)
    type_8_payload_len_percentile = getPercentile(type_8_payload_len_list)

    return [type_0_packet_per_IPPair, type_3_packet_per_IPPair, type_8_packet_per_IPPair, src_ip_amount] + type_0_payload_len_percentile + type_8_payload_len_percentile



def getICMPPayloadLen(data):
    ip_packet = data.payload
    icmp_packet = ip_packet.payload
    icmp_payload = icmp_packet.payload

    return len(icmp_payload.original)

def extractPayloadLenFeature(datas):
    
    icmp_payload_len_list = []
    for data in datas:
        icmp_payload_len = getICMPPayloadLen(data)
        icmp_payload_len_list.append(icmp_payload_len)
    
    return icmp_payload_len_list

def getPercentile(payload_len_list):
    if len(payload_len_list) == 0:
        return [0] * 6
    min = np.percentile(payload_len_list, 0)
    first_quantile = np.percentile(payload_len_list, 25)
    median = np.percentile(payload_len_list, 50)
    third_quantile = np.percentile(payload_len_list, 75)
    max = np.percentile(payload_len_list, 100)
    mean = np.mean(payload_len_list)

    return [min, first_quantile, median, third_quantile, max, mean]


def extractFeaturesWithMultithreading(ip_pair_datas, features, is_negative_sample):
    
    # print(is_negative_sample)  # Value('is_negative_sample', False)
    feature_from_payload_len = extractFeaturesFromPayloadLen(ip_pair_datas)
    print(feature_from_payload_len)

    distance_in_ICMP_pair_list = getDistanceInICMPPair(ip_pair_datas)
    distance_in_ICMP_pair_percentile = getPercentile(distance_in_ICMP_pair_list)
    # print(distance_in_ICMP_pair_list)
    # print(len(distance_in_ICMP_pair_list))
    # print(distance_in_ICMP_pair_percentile)
    # print("\n")

    distance_between_type_8_list = getDistanceBetweenSameside(ip_pair_datas, 8)
    distance_between_type_8_percentile = getPercentile(distance_between_type_8_list)
    # print(distance_between_type_8_list)
    # print(len(distance_between_type_8_list))
    # print(distance_between_type_8_percentile)
    # print("\n")

    distance_between_type_0_list = getDistanceBetweenSameside(ip_pair_datas, 0)
    distance_between_type_0_percentile = getPercentile(distance_between_type_0_list)
    # print(distance_between_type_0_list)
    # print(len(distance_between_type_0_list))
    # print(distance_between_type_0_percentile)
    # print("\n")

    feature_vec = feature_from_payload_len + distance_in_ICMP_pair_percentile + distance_between_type_8_percentile + distance_between_type_0_percentile
    
    if is_negative_sample.Value:
        feature_vec.append(1)
    else :
        feature_vec.append(0)

    features.append(feature_vec)




def extractFeaturesFromIPPairs(pcap_dir, feature_file, is_negative_sample):

    # extractFeaturesFromIPPairs 函数中修改全局变量（如ip_pairs_dict等），这些修改在extractFeaturesWithMultithreading函数无效，可能是因为它们在不同的进程。
    pool = Pool(10)

    manager = Manager()
    ip_pair_datas = manager.list()
    features = manager.list()
    is_negative_sample_para = manager.Value('is_negative_sample', is_negative_sample)

    ip_pairs_dict = {}
    get_filelist(pcap_dir, ip_pairs_dict)

    ip_keys = list(ip_pairs_dict.keys())

    for ip_key in ip_keys:
        ip_pair_datas = ip_pairs_dict.get(ip_key)  
        # 异步方式添加到进程池内
        pool.apply_async(extractFeaturesWithMultithreading, (ip_pair_datas, features, is_negative_sample_para))   

    # 关闭进程池(停止添加，已添加的还可运行)
    pool.close()
    # 让主进程阻塞，等待子进程结束
    pool.join()

    # 1. 创建文件对象
    f = open(feature_file,'a',encoding='utf-8', newline='')

    # 2. 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)

    # 3. 构建列表头
    header_list = ["type_0_packet_per_IPPair", "type_3_packet_per_IPPair", "type_8_packet_per_IPPair", "src_ip_amount"]
    auxiliary_list1 = ["type_0_payload_len_percentile", "type_8_payload_len_percentile", "distance_in_ICMP_pair_percentile", "distance_between_type_8_percentile", "distance_between_type_0_percentile"]
    aux_list2 = ["0", "25", "50", "75", "100", "mean"]
    for item1 in auxiliary_list1:
        for item2 in aux_list2:
            if item2 is "mean":
                header = item1[:-10] + item2
            else:
                header = item1 + '_' + item2
            header_list.append(header)
    
    header_list.append("label")
    csv_writer.writerow(header_list)

    for feature_vec in features:
        csv_writer.writerow(feature_vec)
    f.close()

    
