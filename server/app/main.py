import nmap
from database.connect import connect
from database.insert import insert
from database.delete import delete

connect()   #check connection

# delete('devices')

nmScan = nmap.PortScanner()    # initialize the port scanner

scanRange = nmScan.scan(hosts="192.168.1.0/24", arguments="-O")
# nmScan.scan('127.0.0.1', arguments='-O')


for host in nmScan.all_hosts():
    ipAddress = host
    if(nmScan[host]['vendor']):
        vendor = nmScan[host]['vendor']
        values_view = vendor.values()
        value_iterator = iter(values_view)
        vendor = next(value_iterator)
    else:
        vendor = "unknown"
    if(nmScan[host]['osmatch']):
        os = nmScan[host]['osmatch'][0]['name']
        osFamily = nmScan[host]['osmatch'][0]['osclass'][0]['osfamily']
        osGen = nmScan[host]['osmatch'][0]['osclass'][0]['osgen']
    else:
        os = 'unknown'
        osFamily = 'unknown'
        osGen = 'unknown'
    name = nmScan[host].hostname()

    openPorts = 0
    for proto in nmScan[host].all_protocols():
        print('----------')
        print('Protocol : %s' % proto)
        lport = nmScan[host][proto].keys()
        for port in lport:
            openPorts += 1
            print('port : %s  ' % port)
            print('state : %s' % nmScan[host][proto][port]['state'])

    numOfVulns = 0
    insert(ipAddress, os, name, vendor, osFamily, osGen ,numOfVulns, openPorts)  

