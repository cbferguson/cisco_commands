from netmiko import ConnectHandler
import getpass

#prompts user for username and password
user = input("Enter your username: ")
pword = getpass.getpass()

#add switch IPs to hosts.txt file, 1 on each line
switches = open('hosts.txt', 'r')

#enter the commands that you want to send to the switch
config_commands = [
        'aaa new-model',
        'aaa group server radius radius-duo-group',
        'server name duo',
        'aaa authentication login VTY_authen group radius group radius-duo-group local',
        'aaa authentication enable default none',
        'aaa authorization exec default group radius group radius-duo-group local if-authenticated',
        'aaa authorization exec VTY_author group radius group radius-duo-group local',
        'aaa accounting exec default',
        'ip radius source-interface VlanXXX',
        'radius server duo',
        'address ipv4 X.X.X.X auth-port 1812 acct-port 1813',
        'key XXXXXXXX',
        'line vty 0 4',
        'authorization exec VTY_author',
        'login authentication VTY_authen',
        'transport input ssh',
        'line vty 5 15',
        'authorization exec VTY_author',
        'login authentication VTY_authen',
        'transport input ssh',
        'exit',
        'exit'
        ]

for host in switches:
    host = host.strip()
    cisco_devices = {
        'device_type': 'cisco_ios',
        'ip': host,
        'username': user,
        'password': pword, 
    }

        
    try:
        net_connect = ConnectHandler(**cisco_devices)
        main_commands = net_connect.send_config_set(config_commands)
        wr_me_command = net_connect.send_command_expect('write mem')
        #reload_command = net_connect.send_command('reload', expect_string='Proceed with reload')
        #reload_command_timer = net_connect.send_command_timing('\n')
        print(main_commands)
        print(wr_me_command)
        #print(reload_command)
    except ValueError:
        print("error")