
def getIPPairs(data, ip_pairs_dict):

    if(is_icmp(data)):
        ip_packet = data.payload
        src_ip = ip_packet.fields['src']
        dst_ip = ip_packet.fields['dst']

        key1 = (src_ip, dst_ip)
        key2 = (dst_ip, src_ip)

        if key1 not in ip_pairs_dict.keys() and key2 not in ip_pairs_dict.keys():
            ip_pairs_dict[key1] = []

        if key1 in ip_pairs_dict.keys():
            ip_pairs_dict[key1].append(data)
        elif key2 in ip_pairs_dict.keys():
            ip_pairs_dict[key2].append(data)

def is_icmp(data):
    
    ip_packet = data.payload


    # linux ICMPv4 
    if 'proto' in data.fields.keys() and  data.fields['proto'] == 2048 and ip_packet.fields['proto'] == 1:
        return True

    # Destination unreachable ICMPv4 
    if data.fields['type'] == 2 and ip_packet.fields['proto'] == 1:
        return True

    # ICMPv4 
    if data.fields['type'] == 2048 and ip_packet.fields['proto'] == 1:
        return True
 
    # ICMPv6
    if data.fields['type'] == 34525 and ip_packet.fields['nh'] == 58:
        return True
    
    return False

    # return (data.fields['type'] == 2048 and ip_packet.fields['proto'] == 1) or (data.fields['type'] == 34525 and ip_packet.fields('nh') == 'ICMPv6')
