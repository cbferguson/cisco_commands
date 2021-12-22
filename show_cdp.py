from netmiko import ConnectHandler
import getpass
import json

#prompts user for username and password
user = input("Enter your username: ")
pword = getpass.getpass()

#create a txt file with the seed IP address and add a new line 
switches = open('home_hosts.txt', 'r+')

#connects to the device, runs show cdp neighbor command, dumps the data to JSON format 
#and used the textfsm module from netmiko in order to parse the data accordingly
for host in switches:
    host = host.strip()
    cisco_devices = {
        'device_type': 'cisco_ios',
        'ip': host,
        'username': user,
        'password': pword, 
    }
    try:
        with open('home_hosts.txt', 'r+') as f:
            f.seek(0)
            net_connect = ConnectHandler(**cisco_devices)
            show_cdp_neighbor_detail = net_connect.send_command('show cdp neighbors detail',use_textfsm=True)
            print(json.dumps(show_cdp_neighbor_detail, indent=2))
            for ip_address in show_cdp_neighbor_detail:
                f.seek(0)
                if (ip_address['platform'].__contains__("cisco")):
                    #print("platform contains the word cisco")
                    if ip_address['management_ip'] != 'unassigned':
                        f.seek(0)
                        for line in f.readlines():
                            if line.strip('\n') == ip_address['management_ip']:
                                print('duplicate IP, skipping....')
                                break
                        else:
                            f.write(ip_address['management_ip'])
                            f.write('\n')
    except ValueError:
        print("error")
