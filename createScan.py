from tenable_io.client import TenableIOClient
from tenable_io.api.scans import ScanLaunchRequest
from tenable_io.api.models import ScanSettings
import datetime
import configparser
import io

#This creates the name of the report, which is the current datetime the scan was launched 
currentDateTime = datetime.datetime.now()
reportName = currentDateTime.strftime("%Y"+"%m"+"%d"+"T"+"%H"+"%M")

#This block parses through the ARP table data and creates a list of unique IPs to scan
ipFile = open("test.log", "r")
ipList = list()
for line in ipFile:
    stripedLine = line.rstrip()
    if '.' in stripedLine:
        ipList.append(stripedLine)
    else:
        pass
    for item in ipList:
        if item.startswith(('1','2','3','4','5','6','7','8','9','0')):
            pass
        else:
            ipList.remove(item)
        finalList = [i.split(' ')[0] for i in ipList]    
        
ipFile.close()

#This block imports the API keys from an ini file.
parser = configparser.ConfigParser()
parser.read('tenable_io.ini')
accessKey = parser.get('tenable_io', 'access_key')
secretKey = parser.get('tenable_io', 'secret_key')

#This block launches the Tenable scan.
client = TenableIOClient(access_key=accessKey, secret_key=secretKey)
scanners = {scanner.name: scanner.id for scanner in client.scanners_api.list().scanners}
scans = {scan.name: scan.id for scan in client.scans_api.list().scans}
scan_id = client.scans_api.launch(
 #SCAN ID GOES HERE,
 ScanLaunchRequest(
 alt_targets=finalList
 )
)

#This block downloads the scan report with the date and time the scan was started as the name.
scan = client.scan_helper.id(scans['#NAME OF SCAN GOES HERE'])
scan.download(reportName + '.pdf')
