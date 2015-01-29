from scapy.all import *

global MESSAGE, LWC, SIZE
MESSAGE=''
LWC=False

def UDP_Filter(pack):
    return UDP in pack and Raw in pack and pack[Raw].load=="CODE"

def DeCODE(pack):
    global MESSAGE,LWC
    ch=chr(pack[UDP].dport)
    MESSAGE += ch
    if ch==':':#FIRST ':'
        LWC=True
    elif ch==';' and LWC: #SECOND ';'
        MESSAGE=MESSAGE[:-2]
        print MESSAGE
        LWC=False
        MESSAGE=''
    else: #NO ':'
        LWC=False
def Export_Size(pack):
    global SIZE
    SIZE=pack[UDP].dport
def main():
    #global MESSAGE, LWC
    while True:
        Len_Pack=sniff(count=1, lfilter=UDP_Filter, prn=Export_Size)
        packs=sniff(count=SIZE, lfilter=UDP_Filter, prn=DeCODE)

main()
