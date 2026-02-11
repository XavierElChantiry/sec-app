from scapy.all import sniff

def packet_callback(packet):
    # print(packet.json())  #un comment this one if you want to test the http only one. 
    print(packet.summary())

# a. TCP only
# print("50 TCP packets...")
# sniff(filter="tcp", count=50, prn=packet_callback)

# b. HTTP (port 80)
# print("50 HTTP packets...")
# sniff(filter="tcp port 80", count=50, prn=packet_callback)

# c. DNS (port 53)
print("50 DNS packets...")
sniff(filter="udp port 53", count=50, prn=packet_callback)