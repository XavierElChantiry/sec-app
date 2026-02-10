from scapy.all import rdpcap, IP
from collections import defaultdict

# Detection rule: more than 20 packets in 5 seconds [cite: 77]
THRESHOLD = 20
WINDOW_SIZE = 5 

# Load the PCAP file [cite: 68]
packets = rdpcap("botnet-capture-20110812-rbot.pcap")

# Data structures for tracking [cite: 74]
ip_timestamps = defaultdict(list)
alerted_ips = set()
stats = {"TCP": 0, "UDP": 0}

for pkt in packets:
    if IP in pkt:
        src_ip = pkt[IP].src
        timestamp = float(pkt.time)
        
        # Track protocols for summary [cite: 80, 81]
        if pkt.haslayer("TCP"): stats["TCP"] += 1
        if pkt.haslayer("UDP"): stats["UDP"] += 1

        # Sliding window logic [cite: 75]
        ip_timestamps[src_ip].append(timestamp)
        # Remove timestamps outside the 5-second window
        ip_timestamps[src_ip] = [t for t in ip_timestamps[src_ip] if timestamp - t <= WINDOW_SIZE]

        # Trigger alert if threshold exceeded [cite: 77, 78]
        if len(ip_timestamps[src_ip]) > THRESHOLD and src_ip not in alerted_ips:
            print(f"ALERT: Potential Flooding Detected from {src_ip}")
            alerted_ips.add(src_ip)

# Print final summary [cite: 79, 82]
print(f"\nTotal TCP: {stats['TCP']} | Total UDP: {stats['UDP']}")
print(f"Suspicious IPs Detected: {len(alerted_ips)}")