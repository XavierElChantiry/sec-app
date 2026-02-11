from scapy.all import sniff, Raw

def detect_sensitive_data(packet):
    if packet.haslayer(Raw):
        payload = packet[Raw].load.decode(errors='ignore')
        
        # Keywords I asked AI to come up with
        sensitive_keywords = ['user', 'pass', 'login', 'set-cookie', 'server']
        
        for keyword in sensitive_keywords:
            if keyword in payload.lower():
                print(f"\nkeyword matched somthing may be here")
                print(f"Keyword match: {keyword}")
                print(f"Payload Fragment: {payload[:100]}") # chunk of payload

sniff(filter="tcp port 80", count=50, prn=detect_sensitive_data)