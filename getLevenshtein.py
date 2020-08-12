from getICMPPairs import getICMPPair

def normal_leven(str1, str2):
  m, n = len(str1), len(str2)
  q, d, visited = [(0, 0)], 0, set((0, 0))
  while True:
      next = []
      for (w1, w2) in q:
          if str1[w1:] == str2[w2:]:
              return d
          while w1 < m and w2 < n and str1[w1: w1 + 1] == str2[w2: w2 + 1]:
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


def getDistanceInICMPPair(ip_pair_datas):

  icmp_pairs_dict = {}

  for data in ip_pair_datas:
    getICMPPair(data, icmp_pairs_dict)
  
  distance_in_ICMP_pair_list = []
  for icmp_pair_key in icmp_pairs_dict:
      
    icmp_packet_list = icmp_pairs_dict.get(icmp_pair_key)

    has_icmp_request = False
    request_icmp_payload = bytes()
    reply_icmp_payload = bytes()
    distance_in_ICMP_pair = 0

    for icmp_packet in icmp_packet_list:
      icmp_type = icmp_packet.fields['type']
      if icmp_type == 8:
        # 将icmp pair 中 上一对 8 0报文之间的距离添加到列表中，然后将距离清零，来计算当前8 0报文之间的距离
        if has_icmp_request:  # 初始化distance不添加到列表中
          distance_in_ICMP_pair_list.append(distance_in_ICMP_pair)
        request_icmp_payload = str(icmp_packet.payload.original)
        has_icmp_request = True
        distance_in_ICMP_pair = 0

      elif has_icmp_request and icmp_type == 0:
        reply_icmp_payload = str(icmp_packet.payload.original)
          
      if request_icmp_payload != b'' and reply_icmp_payload != b'':
        distance_in_ICMP_pair += normal_leven(request_icmp_payload, reply_icmp_payload)
        # 对于 8 0 8 0 多个这样的对， 每次计算完距离后，将reply_icmp_payload置空，防止第二个8与与上一个0 算距离
        reply_icmp_payload = b''
    
    # 将icmp pair中最后一对 8 0报文之间的距离添加到列表中
    distance_in_ICMP_pair_list.append(distance_in_ICMP_pair)
  return distance_in_ICMP_pair_list


def getDistanceBetweenSameside(ip_pair_datas, type_code):

  # prev = bytes()
  packet_payload = bytes()
  distance_between_same_side = 0
  distance_between_same_side_list = []

  for data in ip_pair_datas:
    ip_packet = data.payload
    try:
      icmp_packet = ip_packet.payload
      icmp_fields = icmp_packet.fields
      icmp_type = icmp_fields['type']

      if icmp_type == type_code:

        prev = packet_payload
        packet_payload = str(icmp_packet.payload.original)

        if prev != b'' and packet_payload != b'':

          distance_between_same_side = normal_leven(prev, packet_payload)
          distance_between_same_side_list.append(distance_between_same_side)

    except KeyError as e:
      print(ip_packet.fields['src'])
      print(len(data.original))
      print(len(icmp_packet.original))
      print(icmp_packet.original.hex())
      print(e)
      pass
      
    
  return distance_between_same_side_list

