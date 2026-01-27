
import sys
# Add the full path to custom module directory
# sys.path.append('lab2/Lib/site-packages/nmap') 
try:
    import nmap

    import re
    nm = nmap.PortScanner()

    host_to_scan = "127.0.0.1"

    # invalid ip's
    # host_to_scan = "127.0.0"
    # host_to_scan = "127.0.0.5.1"

    #down host
    # host_to_scan = "198.0.2.1"

    port_range = '22-1024'

    # no open port range
    # port_range = '22-102'
    ipv4_pattern = "^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

    try:
        if re.match(ipv4_pattern, host_to_scan):
            nm.scan(host_to_scan, port_range)
            #timeout using all them ports
            # nm.scan('127.0.0.1', '22-40043', timeout=10)

            host_down = True
            # this is how the docs say to do it, so this is how i will do it
            for host in nm.all_hosts():
                print('----------------------------------------------------')
                print('Host : %s (%s)' % (host, nm[host].hostname()))
                print('State : %s' % nm[host].state())
                if nm[host].state() == "up":
                    host_down = False
                for proto in nm[host].all_protocols():
                    print('----------')
                    print('Protocol : %s' % proto)
                    lport = nm[host][proto].keys()
                    for port in sorted(lport):
                        print ('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))
                        print (f'port : {port}\tstate : {nm[host][proto][port]['state']}\tname : {nm[host][proto][port]['name']}\tproduct :  {nm[host][proto][port]['product']}')
                if nm[host].all_protocols() == []:
                    print("no open ports found for this host")

            if host_down:
                print(f"Host : {host_to_scan}\nState : Down/Unreachable")
            
        else:
            print("host input is not an ip address")
    except nmap.PortScannerTimeout:
        print("Nmap scan timed out.")
    except Exception as e:
        print(f"An error occurred: {e}")

except:
    print("you do not have nmap and/or python-nmap")