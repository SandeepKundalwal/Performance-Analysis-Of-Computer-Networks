# shebang does not work over all platforms
# ping.py  2016-02-25 Rudolf
# subprocess.call() is preferred to os.system()
# works under Python 2.7 and 3.4
# works under Linux, Mac OS, Windows

#################################################################################################################################################


# IMPORTING Libraries
import re
import matplotlib.pyplot as plt
import json
import gmplot
import urllib.request
import ipaddress
import platform
from subprocess import Popen, PIPE

averageDelays = []
throughputs = []
#####################################################################################################
#                                   Pinging Hosts                                                   #
#####################################################################################################
def pingHost(hostName):
    avg_RTTS = []
    regex = re.compile("Average = (\d+\S+)")
    ping_str = "-n 10" if  platform.system().lower()=="windows" else "-c 1"
    for i in range(3):
        pingCmd = Popen("ping "  + " " + ping_str + " " + hostName, shell = True, stdout=PIPE, encoding='utf-8')
        for lines in pingCmd.stdout:
            # print(lines)
            line = lines.strip()
            avg_RTT = regex.search(line)
            if avg_RTT is not None:
                val = avg_RTT.group(0).split("=")[1].strip()
                
                s = [float(s) for s in re.findall(r'-?\d+\.?\d*', val)]
                avgDelay = s[0]/1000
                averageDelays.append(avgDelay)
                print("Average Delay = ", avgDelay)
                thoroughput =  32/avgDelay
                throughputs.append(thoroughput)
                print("Throughput = ", thoroughput)



#####################################################################################################
#                                   Running Tracert                                                 #
#####################################################################################################
def runTracert(hostName):
    # running the command 'tracert'
    tracertCmd = Popen("cmd /c tracert " + hostName, shell=True, stdout=PIPE, encoding='utf-8')
    # compiling the regex of IP Address Format
    regex = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    # list to store all the hop IP Addresses
    IPAddressList = []

    for hops in tracertCmd.stdout:
        hop = (hops.strip())
        print(hop)
        # declaring the regex pattern for IP addresses
        IPAddress = regex.search(hop)
        if IPAddress is not None:
            IPAddressList.append(IPAddress.group(0))

    IPAddressList.pop(0)

    return IPAddressList


#####################################################################################################
#                          To get the coordinates of the IP Address                                 #
#####################################################################################################
def getCoordinatesIPAddress(IPAddressList, index):
    latitudes = ['22.719569']
    longitudes = ['75.857726']
    GEO_IP_API_URL  = 'http://ip-api.com/json/'
    for IPAddress in IPAddressList:

        # Can be also site URL like this : 'google.com'
        IP_TO_SEARCH    = IPAddress

        # Creating request object to GeoLocation API
        req             = urllib.request.Request(GEO_IP_API_URL+IP_TO_SEARCH)
        # Getting in response JSON
        response        = urllib.request.urlopen(req).read()
        # Loading JSON from text to object
        json_response   = json.loads(response.decode('utf-8'))

        print(json_response)
        
        if ipaddress.ip_address(IP_TO_SEARCH).is_private:
            continue
        else:
            latitudes.append(json_response['lat'])
            longitudes.append(json_response['lon'])

    print("Plotting on google maps...")
    generateRouteOnMap(latitudes, longitudes, index)


#####################################################################################################
#                              To plot the route on google maps                                     #
#####################################################################################################
def generateRouteOnMap(latitudes, longitudes, index):
    gmapOne = gmplot.GoogleMapPlotter(latitudes.pop(0), longitudes.pop(0), 10, apikey="")
    gmapOne.scatter(latitudes, longitudes, 'red', size = 40, marker = 'o')
    gmapOne.plot(latitudes, longitudes, 'black', edge_width=2.5)
    gmapOne.draw("map" + str(index) + ".html")


# 14.139.34.5 -> Roomie's System      //within campus
# www.moneycontrol.com -> 23.210.77.210     //within India
# www.resideo.com -> 152.195.35.91      //outside India

if __name__ == "__main__":
    index = 1
    hostNames = ['14.139.34.5', 'www.moneycontrol.com', 'www.resideo.com']
    for hostName in hostNames:
        print("Pinging " + hostName + "...")
        pingHost(hostName)
        # x_axis = throughputs
        # y_axis = averageDelays
        # plt.plot(x_axis, y_axis, label = "Afternoon Time Result", color="orange")
        # plt.xlabel("Throughput")
        # plt.ylabel("Delay(ms)")
        # plt.grid(visible=True, color="papayawhip")
        # for xy in zip(x_axis, y_axis):                                      
        #     plt.annotate('(%.2f, %.2f)' % (xy), xy=xy, textcoords='data')
        # plt.show()
        # print()
        IPAddressList = []
        # # IpAddressList = ['10.7.0.1', '14.139.34.1', '10.119.234.162', '72.14.195.56', '108.170.251.97', '64.233.174.17', '172.217.160.228']
        print("Running Tracert...")
        IPAddressList = runTracert(hostName)
        print()
        # # print(IpAddressList)
        print("Getting Coordinates of all the IPs...")
        getCoordinatesIPAddress(IPAddressList, index)
        index += 1
    
    
    
    
