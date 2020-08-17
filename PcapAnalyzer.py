from scapy.all import *
from IPPairsGenerator import IPPairsGenerator
import os
# import re


class PcapAnalyzer():
    def __init__(self, ip_pairs_dict):
        self.ip_pairs_dict = ip_pairs_dict
        self.iPPairsGenerator = IPPairsGenerator(self.ip_pairs_dict)

    def analyzePcap(self, filepath):

        print('filepath:' + filepath)
        s1 = PcapReader(filepath)

        No = 1

        try:
            # data 是以太网 数据包
            data = s1.read_packet()

            while data is not None:

                self.iPPairsGenerator.getIPPairs(data, filepath)

                data = s1.read_packet()

                No += 1

            s1.close()
        except EOFError as ex:
            print(filepath)
            print(No)
            print(ex)
            pass
        
    def get_filelist(self, dir):

        if os.path.isfile(dir):
            try:
                self.analyzePcap(dir)
            except Scapy_Exception as e:
                print(e)

        elif os.path.isdir(dir):
            for s in os.listdir(dir):
                newDir = os.path.join(dir, s)
                self.get_filelist(newDir)