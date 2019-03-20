import sys,json,urllib,uuid,getopt;

dns = raw_input("Local DNS IPv4 Address: ")
mikrotik = raw_input("Generate Mikrotik Address List? (Y/N): ")

url = 'https://endpoints.office.com/endpoints/Worldwide?ClientRequestId='+str(uuid.uuid1())
print 'Fetching endpoints....'
data = json.loads(urllib.urlopen(url).read())

urls = []
ips = []

print "Parsing...."

for endpoint in data:
	if endpoint['serviceArea'] <> "Common":
		if 'urls' in endpoint:
			for url in endpoint['urls']:
				if url not in urls:
					if url[0:1] == '*':
						if url[1:] not in urls:
							urls.append(url[1:])
					else:
						urls.append(url)
		if 'ips' in endpoint:
			for ip in endpoint['ips']:
				if ip not in ips and '.' in ip:
					ips.append(ip)

print "Writing dnsmasq conf...."

with open('o365.conf','w') as f:
	for url in urls:
		f.write("\nserver=/"+url+"/"+dns)
if mikrotik.lower() == 'y':
	with open('o365_mikrotik.rsc','w') as f:
		for ip in ips:
			f.write("\n/ip firewall address-list add address=%s list=o365" % ip)

print "o365.conf		-	dnsmasq conf file"
print "o365_mikrotik.rsc	-	mikrotik address list"
print "Done."

