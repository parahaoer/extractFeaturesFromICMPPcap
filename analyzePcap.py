from scapy.all import *
from getIPPairs import getIPPairs
import re

def analyzePcap(filepath, ip_pairs_dict):
    
    print('filepath:' + filepath)
    s1 = PcapReader(filepath)

    No = 1
  
    try:
        # data 是以太网 数据包
        data = s1.read_packet()
    
        while data is not None:

            getIPPairs(data, ip_pairs_dict)
            
            data = s1.read_packet() 

            No += 1

        s1.close()
    except EOFError as ex:
        print(filepath)
        print(No)
        print(ex)
        pass
        
        
def get_filelist(dir, ip_pairs_dict):

    if os.path.isfile(dir):
        try:
            analyzePcap(dir, ip_pairs_dict)        
        except Scapy_Exception as e:
            print(e)

    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            get_filelist(newDir, ip_pairs_dict)