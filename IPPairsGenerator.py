import os


class IPPairsGenerator():
    def __init__(self, ip_pairs_dict):

        self.ip_pairs_dict = ip_pairs_dict

    def jwkj_get_filePath_fileName_fileExt(self, file_path):
        (filepath, tempfilename) = os.path.split(file_path)
        (shortname, extension) = os.path.splitext(tempfilename)
        # filepath是文件所在的目录（最后没有 /），shotname是去除最后一个. 所得到的文件名
        return filepath, shortname, extension

    def getNegativeFlag(self, file_path):
        file_path, shortname, _ = self.jwkj_get_filePath_fileName_fileExt(
            file_path)
        if 'negative' in file_path:
            return 'negative_' + shortname
        elif 'positive' in file_path:
            return 'positive_' + shortname

    def getIPPairs(self, data, file_path):

        if (self.is_icmp(data)):
            ip_packet = data.payload
            src_ip = ip_packet.fields['src']
            dst_ip = ip_packet.fields['dst']

            key1 = (self.getNegativeFlag(file_path) + src_ip,
                    self.getNegativeFlag(file_path) + dst_ip)
            key2 = (self.getNegativeFlag(file_path) + dst_ip,
                    self.getNegativeFlag(file_path) + src_ip)

            if key1 not in self.ip_pairs_dict.keys(
            ) and key2 not in self.ip_pairs_dict.keys():
                self.ip_pairs_dict[key1] = []

            if key1 in self.ip_pairs_dict.keys():
                self.ip_pairs_dict[key1].append(data)
            elif key2 in self.ip_pairs_dict.keys():
                self.ip_pairs_dict[key2].append(data)

    def is_icmp(self, data):

        ip_packet = data.payload
        data_fields = data.fields

        # linux ICMPv4
        if 'proto' in data_fields.keys(
        ) and data_fields['proto'] == 2048 and ip_packet.fields['proto'] == 1:
            return True

        # Destination unreachable ICMPv4
        if data_fields['type'] == 2 and ip_packet.fields['proto'] == 1:
            return True

        # ICMPv4
        if data_fields['type'] == 2048 and ip_packet.fields['proto'] == 1:
            return True

        # ICMPv6
        if data_fields['type'] == 34525 and ip_packet.fields['nh'] == 58:
            return True

        return False

        # return (data.fields['type'] == 2048 and ip_packet.fields['proto'] == 1) or (data.fields['type'] == 34525 and ip_packet.fields('nh') == 'ICMPv6')
