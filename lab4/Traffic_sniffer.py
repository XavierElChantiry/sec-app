from scapy.all import sniff, IP, TCP, UDP

# Dictionary to store protocol counts [cite: 61]
protocol_counts = {"TCP": 0, "UDP": 0, "Other": 0}

def packet_callback(packet):
    # Extract details for Parts 2 and 4 [cite: 49, 60]
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        proto = "TCP" if packet.haslayer(TCP) else "UDP" if packet.haslayer(UDP) else "Other"
        
        # Update counts [cite: 61]
        if proto in protocol_counts:
            protocol_counts[proto] += 1
            
        print(f"[{proto}] {src_ip} -> {dst_ip}")

# Capture 50 packets [cite: 39, 44]
print("Starting live capture...")
sniff(count=50, prn=packet_callback)

# Output summary [cite: 62]
print("\n--- Capture Summary ---")
for proto, count in protocol_counts.items():
    print(f"{proto}: {count}")