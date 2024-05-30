import requests
import socket
import threading

class IPStresser:
    def __init__(self, url, num_requests):
        self.url = url
        self.num_requests = num_requests

    def generate_ip_addresses(self):
        for _ in range(self.num_requests):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip_address = sock.getsockname()[0]
            yield ip_address
            sock.close()

    def send_requests(self):
        for ip_address in self.generate_ip_addresses():
            headers = {
                "X-Forwarded-For": ip_address,
                "Client-IP": ip_address
            }
            response = requests.get(self.url, headers=headers)

if __name__ == "__main__":
    url = input("Podaj adres URL twojej strony: ")
    num_requests = int(input("Podaj ilość requests: "))

    stresser = IPStresser(url, num_requests)
    threading.Thread(target=stresser.send_requests).start()

    print("Wygenerowano {} request'ów z różnych adresów IP.".format(num_requests))