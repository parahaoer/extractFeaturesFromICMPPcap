from ICMPPairsGenerator import ICMPPairsGenerator
from ICMPSessionGenerator import ICMPSessionGenerator


class LevenshteinDistanceCalculator():
    def __init__(self, ip_pair_datas):
        self.icmp_pairs_dict = {}
        iCMPPairsGenerator = ICMPPairsGenerator()
        iCMPPairsGenerator.getICMPPair(ip_pair_datas, self.icmp_pairs_dict)

        self.icmp_session_dict = {}
        iCMPSessionGenerator = ICMPSessionGenerator()
        iCMPSessionGenerator.getICMPSession(ip_pair_datas, self.icmp_session_dict)

    def normal_leven(self, str1, str2):
        m, n = len(str1), len(str2)
        q, d, visited = [(0, 0)], 0, set((0, 0))
        while True:
            next = []
            for (w1, w2) in q:
                if str1[w1:] == str2[w2:]:
                    return d
                while w1 < m and w2 < n and str1[w1:w1 + 1] == str2[w2:w2 + 1]:
                    w1 += 1
                    w2 += 1
                if w2 < n and (w1, w2 + 1) not in visited:
                    next.append((w1, w2 + 1))
                    visited.add((w1, w2 + 1))
                if w1 < m and (w1 + 1, w2) not in visited:
                    next.append((w1 + 1, w2))
                    visited.add((w1 + 1, w2))
                if w1 < m and w2 < n and (w1 + 1, w2 + 1) not in visited:
                    next.append((w1 + 1, w2 + 1))
                    visited.add((w1 + 1, w2 + 1))
            q = next
            d += 1

    def getDistanceInICMPPair(self):

        # print('icmp_pairs_dict_len=' + str(len(icmp_pairs_dict)))
        distance_in_ICMP_pair_list = []
        for icmp_pair_key in self.icmp_pairs_dict:

            icmp_packet_list = self.icmp_pairs_dict.get(icmp_pair_key)

            has_icmp_request = False
            request_icmp_payload = b'init'
            reply_icmp_payload = b'init'
            distance_in_ICMP_pair = 0

            for icmp_packet in icmp_packet_list:
                icmp_type = icmp_packet.fields['type']
                if icmp_type == 8:
                    # 将icmp pair 中 上一对 8 0报文之间的距离添加到列表中，然后将距离清零，来计算当前8 0报文之间的距离
                    if has_icmp_request:  # 初始化distance不添加到列表中
                        distance_in_ICMP_pair_list.append(distance_in_ICMP_pair)
                    request_icmp_payload = icmp_packet.payload.original
                    has_icmp_request = True
                    distance_in_ICMP_pair = 0

                elif has_icmp_request and icmp_type == 0:
                    reply_icmp_payload = icmp_packet.payload.original

                if request_icmp_payload != b'init' and reply_icmp_payload != b'init':
                    distance_in_ICMP_pair += self.normal_leven(request_icmp_payload, reply_icmp_payload)
                    # 对于 8 0 8 0 多个这样的对， 每次计算完距离后，将reply_icmp_payload置空，防止第二个8与与上一个0 算距离
                    reply_icmp_payload = b'init'

            # 将icmp pair中最后一对 8 0报文之间的距离添加到列表中
            if has_icmp_request:
                distance_in_ICMP_pair_list.append(distance_in_ICMP_pair)
        return distance_in_ICMP_pair_list

    def getDistanceBetweenSameside(self, type_code):

        packet_payload = b'init'

        distance_between_same_side_list = []

        for id in self.icmp_session_dict:
            distance_between_same_side_in_icmp_session = []
            for icmp_packet in self.icmp_session_dict[id]:

                icmp_fields = icmp_packet.fields
                icmp_type = icmp_fields['type']

                if icmp_type == type_code:

                    prev = packet_payload
                    packet_payload = icmp_packet.payload.original

                    distance_between_same_side = self.normal_leven(prev, packet_payload)
                    distance_between_same_side_in_icmp_session.append(distance_between_same_side)
            # 去掉列表中第一个冗余的元素
            distance_between_same_side_in_icmp_session = distance_between_same_side_in_icmp_session[1:]
            distance_between_same_side_list += distance_between_same_side_in_icmp_session
        return distance_between_same_side_list
