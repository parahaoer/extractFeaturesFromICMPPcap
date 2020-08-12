def getICMPPair(data, icmp_pairs_dict):

    ip_packet = data.payload
    
    icmp_packet = ip_packet.payload

    icmp_fileds = icmp_packet.fields

    try:

        icmp_type = icmp_fileds['type']

        if icmp_type == 8 or icmp_type == 0:

            id = icmp_packet.fields['id']
            seq = icmp_packet.fields['seq']
            key = (id, seq)
            
            if key not in icmp_pairs_dict.keys():

                icmp_pairs_dict[key] = []

            icmp_pairs_dict[key].append(icmp_packet)
    except KeyError as e:
        print(ip_packet.fields['src'])
        # print(len(data.payload.payload.original))
        print(e)
        pass

