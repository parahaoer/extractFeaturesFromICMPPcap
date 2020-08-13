from scapy.all import *
from getIPPairs import getIPPairs
import re


def jwkj_get_filePath_fileName_fileExt(filename):
    (filepath,tempfilename) = os.path.split(filename)
    (shortname,extension) = os.path.splitext(tempfilename)
    #filepath是文件所在的目录（最后没有 /），shotname是去除最后一个. 所得到的文件名
    return filepath,shortname,extension

def analyzePcap(filepath, ip_pairs_dict):
    
    _, shortname, _ = jwkj_get_filePath_fileName_fileExt(filepath)
    print('filepath:' + filepath)
    s1 = PcapReader(filepath)

    No = 1
  
    try:
        # data 是以太网 数据包
        data = s1.read_packet()
    
        while data is not None:

            getIPPairs(data, ip_pairs_dict, shortname)
            
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