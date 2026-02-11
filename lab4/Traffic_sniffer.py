from scapy.all import sniff, IP, IPv6, TCP, UDP, Ether
from collections import Counter

# like counter i think its better than a dict for this job
protocol_stats = Counter()

def traffic_analyzer(packet):
    # IPv4
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        proto_num = packet[IP].proto
    # IPv6
    elif IPv6 in packet:
        src_ip = packet[IPv6].src
        dst_ip = packet[IPv6].dst
        proto_num = packet[IPv6].nh  # 'nh' is beside the header. took to long to realize
    else:
        # other is things like arp or ethernet
        print(f"Non ip based network traffic: {packet.summary()}")
        # print(packet.summary()) # this was for debug
        protocol_stats["Other"] += 1
        return

    # UDP and TCP are most offten so they get special treatment 
    if packet.haslayer(TCP):
        protocol = "TCP"
        sport, dport = packet[TCP].sport, packet[TCP].dport
    elif packet.haslayer(UDP):
        protocol = "UDP"
        sport, dport = packet[UDP].sport, packet[UDP].dport
    else:
        protocol = f"Proto-{proto_num}"
        sport = dport = "N/A"

    # printing to termina is my logging
    protocol_stats[protocol] += 1
    print(f"{protocol:8} | {src_ip} -> {dst_ip} | Ports: {sport}->{dport}")

print("capturing of 50 packets (IPv4 & IPv6) its 2026 IPv6 needed")
try:
    sniff(prn=traffic_analyzer, count=50) 
except PermissionError:
    print("Error: run as sudo/admin")

print("\n--- Final Protocol Summary ---")
for proto, count in protocol_stats.items():
    print(f"{proto}: {count}")