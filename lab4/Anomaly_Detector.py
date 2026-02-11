from scapy.all import rdpcap, IP, TCP, UDP


pcap = "botnet-capture-20110812-rbot.pcap" 
threshold = 20  
slidingwindow = 5 

def run_ids_analysis():
    print(f"Loading {pcap}...")
    try:
        packets = rdpcap(pcap)
    except FileNotFoundError:
        print("Error: no pcap")
        return

    ip_timestamps = {} 
    alerted_ips = []   
    
    tcp_count = 0
    udp_count = 0

    for pkt in packets:
        # i am just doing IPv4 as the pcap only deals with IPv4
        if IP in pkt:
            src_ip = pkt[IP].src
            timestamp = float(pkt.time)

            # protocol count
            if pkt.haslayer(TCP): 
                tcp_count += 1
            if pkt.haslayer(UDP): 
                udp_count += 1

            # adding ips to dict so we can count em
            if src_ip not in ip_timestamps:
                ip_timestamps[src_ip] = []
            
            # add ip timestamp to dict
            ip_timestamps[src_ip].append(timestamp)
            

            fresh_timestamps = []
            for t in ip_timestamps[src_ip]:
                # Check if the packet timestamp is within 5 seconds of the current packet
                if (timestamp - t) <= slidingwindow:
                    fresh_timestamps.append(t)
            
            # Update the dictionary with only the "fresh" timestamps
            ip_timestamps[src_ip] = fresh_timestamps

            if len(ip_timestamps[src_ip]) > threshold:
                if src_ip not in alerted_ips:
                    print(f"Warning: threshold exeded {src_ip}")
                    alerted_ips.append(src_ip)

    print("\n--- PCAP SUMMARY ---")
    print(f"total TCP Packets: {tcp_count}")
    print(f"total UDP Packets: {udp_count}")
    print(f"suspicious IPs found: {len(alerted_ips)}")
    for ip in alerted_ips:
        print(f" -> {ip}")


run_ids_analysis()