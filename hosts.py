# If you're rerunning this script after the initial provisioning, run the 
# GetIPAddresses.ps1 powershell script first.  That will refresh the hosts.ini
# data with current ip addresses.

import python_hosts
import configparser

config = configparser.ConfigParser()
config.read("/vagrant/hosts.ini")

hosts = python_hosts.Hosts(path="/etc/hosts")

for entry in config.sections():
    print("entry:", entry)
    entry_type = config[entry]["entry_type"]
    print ("entry_type:", entry_type)
    ip_address = config[entry]["address"]
    print ("ip_address:", ip_address)

    name_list = []
    name = config[entry]["names"]
    print("name:", name)
    for n in name.split(","):
        name_list.append(n)

    # Remove any previous entry in the hosts file for the current name. If a 
    # computer is recreated, this will clear out the previous entry in the
    # hosts file, and replace it with new information.
    hosts.remove_all_matching(name=name)

    new_entry = python_hosts.HostsEntry(
        entry_type=entry_type,
        address=ip_address,
        names=name_list
    )
    hosts.add([new_entry])

hosts.write()
