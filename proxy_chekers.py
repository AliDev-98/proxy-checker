import requests
import time
import argparse
import datetime
import asyncio

class ProxyCheckers:
    def __init__(self):
        self.command()
        
    def command(self):
        parser = argparse.ArgumentParser(description="Read Commands and works ... ")
        parser.add_argument('-p', metavar='--proxy_list', help="Enter the proxy list ", default=None, type=str, required=True)
        args = parser.parse_args()

        self.list_p = args.p

    def get_proxies(self):
        if self.list_p is None:
            print("Enter proxy list ... ")
        else:
            try:
                with open(self.list_p, 'r') as p:
                    proxies = p.read().splitlines()
                    return proxies
            except Exception as e:
                print(f"Error loading proxies file: {e}")

    def proxy_requests(self):
        url = "https://google.com"
        proxies = self.get_proxies()

        if proxies is None:
            return

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        filename = f"working_proxies_{current_time}.txt"
        with open(filename, 'w') as f:
            for proxy in proxies:
                proxies_dict = {"http": proxy, "https": proxy}
                try:
                    response = requests.get(url, proxies=proxies_dict, timeout=2) 
                    if response.status_code == 200:
                        print(f"Proxy {proxy} is working.")
                        f.write(proxy + "\n")
                    else:
                        print(f"Proxy {proxy} is not working.")
                except requests.exceptions.Timeout as T:
                    print(f"Proxy {proxy} Time out")
                except requests.exceptions.RequestException as e:
                    print(f"Error connecting to proxy {proxy}: {e}")

if __name__ == "__main__":
    ProxyCheckers().proxy_requests()
