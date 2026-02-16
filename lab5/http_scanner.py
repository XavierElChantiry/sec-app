import requests
import json

target = "http://localhost:3000"

enpoint = [
    "/", 
    "/rest/products/search", 
    "/rest/user/login",
    "/api/Feedbacks",
    "/rest/basket",
    "/ftp"
]

injection = [
    ("normal", "apple"),
    ("normal", "a"),
    ("xss", "<script>alert(1)</script>"),
    ("xss", "<u>test</u>"),
    ("sqli", "' OR 1=1 --"),
    ("sqli", "'")
]

results_data = []


def format_results(endpoint, method, payload_type, payload, response):
    # i output to json  its easier for me that way to check what as sent

    entry = {
        "endpoint": endpoint,
        "method": method,
        "payload_type": payload_type,
        "payload": payload,
        "status_code": response.status_code,
        "response_headers": dict(response.headers),
        "response_body": response.text
    } 
    results_data.append(entry)

    # format table
    p_disp = payload if len(payload) < 20 else payload[:17] + "..."
    print(f"{endpoint:<22} | {method:<6} | {payload_type:<8} | {p_disp:<20} | {response.status_code:<6} | {len(response.text)}")

def main():
    print(f"scanning target: {target}\n")
    # header for table
    header = f"{'Endpoint':<22} | {'Method':<6} | {'Type':<8} | {'Payload':<20} | {'Status':<6} | {'Length'}"
    print(header)
    print("-" * len(header))
    
    for endpoint in enpoint:
        url = target + endpoint
        for payload_type, payload_sent in injection:
            # Test both GET and POST for every combination (Part 2 requirement)
            for method in ["GET", "POST"]:
                try:
                    if method == "GET":
                        # Simulate search or parameter-based interrogation
                        res = requests.get(url, params={'q': payload_sent}, timeout=5)
                    else:
                        # Simulate form submissions (Login/Feedback)
                        data = {"email": payload_sent, "password": payload_sent, "comment": payload_sent}
                        res = requests.post(url, json=data, timeout=5)
                    
                    format_results(endpoint, method, payload_type, payload_sent, res)

                except requests.RequestException as error:
                    print(error)
                    
                    continue


    with open("scan_results.json", "w") as f:
        json.dump(results_data, f, indent=2)
    

if __name__ == "__main__":
    main()