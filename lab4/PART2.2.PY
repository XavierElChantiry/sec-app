from scapy.all import rdpcap, IP, TCP, UDP, Ether


PCAP_FILE = "botnet-capture-20110812-rbot.pcap"
packets = rdpcap(PCAP_FILE)

print(f"Inspecting first 10 packets from {PCAP_FILE}...\n")

for i in range(10):
    pkt = packets[i]
    print(f"--- Packet #{i+1} ---")
    
    
    if Ether in pkt:
        print(f"Ethernet: {pkt[Ether].src} -> {pkt[Ether].dst}")
    
    
    if IP in pkt:
        print(f"IP: {pkt[IP].src} -> {pkt[IP].dst} | Protocol: {pkt[IP].proto}")
        
        
        if pkt.haslayer(TCP):
            print(f"TCP Port: {pkt[TCP].sport} -> {pkt[TCP].dport}")
            print(f"TCP Flags: {pkt[TCP].flags}")
        elif pkt.haslayer(UDP):
            print(f"UDP Port: {pkt[UDP].sport} -> {pkt[UDP].dport}")
    print("-" * 30)