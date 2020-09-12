class ICMPSessionGenerator():
    def getICMPSession(self, ip_pair_datas, icmp_session_dict):
        for data in ip_pair_datas:
            ip_packet = data.payload

            icmp_packet = ip_packet.payload

            icmp_fileds = icmp_packet.fields

            try:

                icmp_type = icmp_fileds['type']

                if icmp_type == 8 or icmp_type == 0:

                    id = icmp_packet.fields['id']

                    if id not in icmp_session_dict.keys():

                        icmp_session_dict[id] = []

                    icmp_session_dict[id].append(icmp_packet)
            except KeyError as e:
                print(ip_packet.fields['src'])
                # print(len(data.payload.payload.original))
                print(e)
