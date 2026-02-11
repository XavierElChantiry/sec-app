from scapy.all import rdpcap, IP, Raw

PCAP_FILE = "botnet-capture-20110812-rbot.pcap"
packets = rdpcap(PCAP_FILE)


sensitive_keywords = ['user', 'pass', 'login', 'cookie', 'server', 'version']

print(f"Scanning {PCAP_FILE} for sensitive data...\n")

found_count = 0
for pkt in packets:
    if pkt.haslayer(Raw):
        
        payload = pkt[Raw].load.decode(errors='ignore').lower()
        
        for word in sensitive_keywords:
            if word in payload:
                found_count += 1
                src_ip = pkt[IP].src if IP in pkt else "Unknown"
                print(f"[!] Match '{word}' found from {src_ip}")
                print(f"    Payload: {payload[:80]}...") 
                break 

print(f"\nScan complete. Total sensitive packets identified: {found_count}")