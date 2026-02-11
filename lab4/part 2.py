from scapy.all import sniff, IP, TCP, UDP

def inspect_packet(pkt):
    if IP in pkt:
        # IP and Protocol
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        proto = pkt[IP].proto
        
        print(f"\n--- New Packet ---")
        print(f"Source: {src_ip} | Dest: {dst_ip} | Proto: {proto}")

        # TCP Ports and Flags
        if pkt.haslayer(TCP):
            print(f"TCP Port: {pkt[TCP].sport} -> {pkt[TCP].dport}")
            print(f"Flags: {pkt[TCP].flags} | Length: {len(pkt)}")
        
        # UDP Port
        elif pkt.haslayer(UDP):
            print(f"UDP Port: {pkt[UDP].sport} -> {pkt[UDP].dport}")

sniff(count=50, prn=inspect_packet)