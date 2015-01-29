from scapy.all import *
import struct

def encodep(label): #I found this one on the internet. It works. I don't know how it works, but I know it does.
    sublabels = label.split(".") + [""]
    label_format = ""

    for s in sublabels:
        label_format = '%s%dp' % (label_format, len(s) + 1)

    label_data = struct.pack(label_format, *sublabels)

    return label_data

def dns_filter(packet):#filter
    return IP in packet and DNS in packet and(packet[DNSQR].qtype in (1, 12)) and packet[IP].dst=="192.168.1.80" #Replace the destination IP with the one of your machine, through which you are listening




def recover_actual_ip(qname): #because PTR is annoying
    parts=qname.split('.')
    actualip=parts[3]+'.'+parts[2]+'.'+parts[1]+'.'+parts[0]
    return actualip

#----------#
def Make_Packet(packet, qn):
    Rpack=IP()/UDP()/DNS()#base packet creation
    #IP
    ##Rpack[IP].src=packet[IP].dst
    Rpack[IP].dst=packet[IP].src
    
    #UDP
    Rpack[UDP].dport=packet[UDP].sport
    Rpack[UDP].sport=packet[UDP].dport
    
    #DNS
    Rpack[DNS].qr=long(1)
    Rpack[DNS].id=packet[DNS].id
    Rpack[DNS].qdcount=1
    Rpack[DNS].ancount=1
    
    #DNSQR
    Rpack[DNS].qd=packet[DNSQR]
    
    #DNSRR
    Rpack[DNS].an=DNSRR()
    Rpack[DNSRR].rclass=1
    
    if packet[DNSQR].qtype == 1:#A type
        Rpack=A_Type(packet, Rpack, qn)
    else: #PTR type
        Rpack=PTR_Type(packet, Rpack, qn)
        
    return Rpack


#--------------------#
def A_Type(packet, Rpack, qn):
    Rpack[DNSRR].type=1#A type
    #Rpack[DNSRR].ttl=300
    Rpack[DNSRR].rrname=qn#rrname and qname should be the same. I think.
    Rpack[DNS].rcode=0
    
    if qn in dct.keys():#everything's ok
        Rpack[DNSRR].rdata=dct[qn][0]
        Rpack[DNSRR].ttl=dct[qn][1]
    else:#no information in dct
        Rpack=Forward_Packet(Rpack, qn)
    return Rpack

def PTR_Type(packet, Rpack, qn):
    Rpack[DNSRR].type=12#PTR type
    #Rpack[DNSRR].ttl=1500
    Rpack[DNS].rcode=0
    Rpack[DNSRR].rrname=qn
    if recover_actual_ip(qn) in reverse_dct.keys():#everything's ok
        Rpack[DNSRR].rdata=encodep(reverse_dct[recover_actual_ip(qn)][0])
        Rpack[DNSRR].ttl=reverse_dct[recover_actual_ip(qn)][1]
    else:#no information in reverce_dct
        Rpack=Forward_Packet(Rpack, qn)
    return Rpack

#------------------------------#



def Forward_Packet(Rpack, qn):
    global dct
    global reverse_dct
    FWpack = IP(dst='8.8.8.8')/UDP(dport=53)/DNS(qr=0,rd=1,qdcount=1)#Change the ip to the external DNS server you want to use
    FWpack[DNS].qd=DNSQR(qname=qn, qtype=Rpack[DNSQR].qtype) 
    RSPpack=sr1(FWpack)#waiting for response
    print "External Server's answer:"
    RSPpack.show()
    if DNSRR in RSPpack and RSPpack[DNS].rcode!=3:#everything is as planned
        for i in xrange(RSPpack[DNS].ancount):#goes through all the recived rrs until it finds what it was looking for
            rr_record=RSPpack[DNS][DNSRR][i]
            if rr_record.type==Rpack[DNSQR].qtype:
                """3"""
                Rpack[DNSRR].ttl=RSPpack[DNSRR].ttl#ttl
                if rr_record.type==1:#A
                    Rpack[DNSRR].rdata=rr_record.rdata#copy the data recived to our response packet
                    Rpack[DNSRR].rrname=rr_record.rrname
                    wrds=qn
                    nums=rr_record.rdata
                    dct[wrds]=(nums, RSPpack[DNSRR].ttl)
                    break
                elif rr_record.type==12:#PTR
                    Rpack[DNSRR].rdata=encodep(rr_record.rdata)#copy the data recived to our response packet
                    Rpack[DNSRR].rrname=rr_record.rrname
                    nums=recover_actual_ip(qn)
                    wrds=Rpack[DNSRR].rdata
                    reverse_dct[nums]=(wrds, RSPpack[DNSRR].ttl)
                    break
        
    else:#something weng wrong... oops
        Rpack=Name_Error(Rpack)
    return Rpack
#----------------------------------------#
"""def Add_To_Cache(wrds, nums):
    dct[wrds]=nums
    reverse_dct[nums]=wrds"""
    
def Name_Error(Rpack):
    Rpack[DNSRR].ttl=3600
    Rpack[DNS].rcode=3
    return Rpack
#----------------------------------------#

def print_stuff():
    global dct
    global reverse_dct
    print "A database:"
    for a in dct.keys():
        print a+" > > > "+dct[a][0]+" ttl: "+str(dct[a][1])
    print "\nPTR database:"
    for ptr in reverse_dct.keys():
        print ptr+" > > > "+reverse_dct[ptr][0]+" ttl: "+str(reverse_dct[ptr][1])
    
    
global dct
global reverse_dct
dct={}
reverse_dct={}



while True:
    print_stuff()
    packets=sniff(count=1, lfilter=dns_filter)#sniff
    send(packets[0])
    packet=packets[0]
    qn=packet[DNSQR].qname
    Rpack=Make_Packet(packet, qn)

    print "My answer:"
    Rpack.show()
    send(Rpack)
