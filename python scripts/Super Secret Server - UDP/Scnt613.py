#global IP
#IP='192.168.1.184'
#===============
from scapy.all import *

def send_len(port, ip):
    p=IP(dst=ip)/UDP(sport=55698, dport=port)/Raw(load="CODE")
    send(p)
        
def main():
    ip=raw_input('Enter the desired ip: ')
    data=raw_input('Enter the massege to send: ')
    data+=':;'
    ln=len(data)
    send_len(ln, ip)
    for ch in data:
        port=ord(ch)
        p=IP(dst=ip)/UDP(sport=55698, dport=port)/Raw(load="CODE")
        send(p)

    print "INFO SENT"

main()
