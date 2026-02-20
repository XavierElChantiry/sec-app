from scapy.all import sniff, IP, IPv6, TCP, UDP

# these 2 are for the logic to alert when packet density gets too high
threshold = 50
sliding_window = 5.0


ip_timestamps = {}
alerted_ips = []


def packet_analyzer(pkt):

    """
    Just below this we are making sure the length of packets matches what they declaire their length to be.
    This is to detect malformed packets. A few is normal, but a lot could be a sign of a scan or attack.
    I have this script running and ralize github loves declairing a len of 40 but sending  46

    """
    if IP in pkt:
        src_ip = pkt[IP].src
        declared_len = pkt[IP].len
        real_len = len(pkt[IP])
        if (declared_len != real_len): # i suggest you add  and src_ip != "ip address" for github servers, as they spam malformed packets
            print(f"\n[malformed packet] from: {src_ip} declares the len of {declared_len} but really had a len of {real_len}")

    elif IPv6 in pkt:
        src_ip = pkt[IPv6].src
        declared_len_ipv6 = pkt[IPv6].plen
        real_len_ipv6 = len(pkt[IPv6].payload)
        # print(declared_len_ipv6, real_len_ipv6) # i was not getting any malfromed from ipv6 so i had to check it was working
        if declared_len_ipv6 != real_len_ipv6:
            print(f"\n[malformed packet] from: {src_ip} declares the len of {declared_len_ipv6} but really had a len of{real_len_ipv6}")
    else:
        return

    """
    in this section we reuse the logic from the anomaly detector in lab4.
    This is looking for flood or scan attacks by seeing if a given ip is sending more 
    """
    current_packet_time = float(pkt.time)

    # adding ips to list so we can keep track of packets sent
    if src_ip not in ip_timestamps:
        ip_timestamps[src_ip] = []
    ip_timestamps[src_ip].append(current_packet_time)

    # here we cull out timestamps from before the sliding window for this ip address
    culled_timestamps = []
    for old_packet in ip_timestamps[src_ip]:
        # here we cut out packets older than the sliding window of seconds.
        # print(current_packet_time, old_packet)
        if (current_packet_time - old_packet) <= sliding_window:
            culled_timestamps.append(old_packet)
    
    ip_timestamps[src_ip] = culled_timestamps

    # clear alerted ips so if this runs forever it does not eat all the RAM
    if len(alerted_ips) > 100:
        alerted_ips.clear()

    """
    as we know syn floods are something we should be extra careful of,
    so we check if the packet that exceeded the threshold was a syn packet, if it was we get an alert
    This is not a perfect method, but it is atleast some indication.
    """
    is_syn = False 
    if TCP in pkt and pkt[TCP].flags == "S":
        is_syn = True

    # threshold check to see if there are more packets than permited in sliding window
    if len(ip_timestamps[src_ip]) > threshold:
        if src_ip not in alerted_ips:
            if is_syn:
                print(f"[SYN FLOOD possible] from {src_ip}")
                print(f"\n[threshhold exceeded] {src_ip} ({len(ip_timestamps[src_ip])} packets in {sliding_window}seconds) ")

            else:
                print(f"\n[threshhold exceeded] by: {src_ip} ({len(ip_timestamps[src_ip])} packets in {sliding_window}seconds)")
            # we add ip to list so we only get one alert when the threshold is reached
            # i could add a timeout so it re apears if the behaviour coninues, but this is just proof of concept.
            alerted_ips.append(src_ip)



def main():
    print("scan starting, end it using Ctrl+C or whatever you keyboard inturrupt is")
    """
    store=0 makes it so that packets are not stored to memory.
    This way it wont eat all the ram on a machine if left running.
    """
    sniff(filter="ip or ip6", prn=packet_analyzer, store=0)

if __name__ == "__main__":

    main()
