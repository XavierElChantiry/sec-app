
import nmap
import datetime



def port_scan(target_ip, target_port):
    nm = nmap.PortScanner()

    nm.scan(target_ip, str(target_port), arguments='-sV')

    log_filename = "recon_log.txt"
    
    with open(log_filename, "w") as log_file:
        log_file.write(f"RECON LOG - {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n")
        log_file.write("\n")
        
        if target_ip in nm.all_hosts():
            state = nm[target_ip].state()
            log_file.write(f"Host: {target_ip}:{target_port} ({state})\n")
            
            # Check if our specific port is found 
            if nm[target_ip].has_tcp(target_port):
                port_data = nm[target_ip]['tcp'][target_port]
                status = port_data['state']
                service = port_data['name']
                version = port_data['version']
                
                output = (f"Port {target_port}: {status}\n"
                          f"Service: {service}\n"
                          f"Version: {version}\n")
                
                print(f"Found Target: \n{output}")
                log_file.write(output)
                if status == "closed":
                    return 
                return "OPEN"
            else:
                log_file.write(f"Port {target_port} is NOT open or was filtered.\n")
                print(f"Warning: Port {target_port} is not responding.")
                return 
        else:
            log_file.write(f"Host {target_ip}:{target_port} is down or unreachable.\n")
            print("Error: Host unreachable.")
            return 





if __name__ == "__main__":
    c = port_scan("localhost", 4726)
    print(c)