# I don't think it's possible to create an idepotent process to manage the
# known_hosts file.  In instances where you destroy and recreate a vm, when
# using Hyperv, the ip address will change.  You can't decode the existing 
# entries in the known_hosts file to see if there are old entries for the host
# name.  For now, the only option I can come up with is to delete and recreate
# the known_hosts file using the hosts.ini data.  Down the road, I may have a
# better solution.  JXS 7/2/2019

import configparser
import os
import subprocess

config = configparser.ConfigParser()
config.read("/vagrant/hosts.ini")

def keyscan_host(host):
    keys_to_write = []

    results = subprocess.run(
        ["ssh-keyscan", "-H", host],
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    output = results.stdout
    output = output.split("\n")

    for line in output:
        if line != "":
            keys_to_write.append(line)
    return keys_to_write

# Delete the known_hosts file if it exists.
known_host_file = "/home/vagrant/.ssh/known_hosts"
if os.path.exists(known_host_file):
    print("Previous hosts file located.  Deleting.")
    os.remove(known_host_file)

host_keys = {}
key_tracking = []

# Generate the key data for the known_hosts file for each server listed in
# the hosts.ini.
for computer in config.sections():
    print(computer)
    keys = keyscan_host(host=config[computer]['address'])
    for key in keys:
        key_tracking.append(key)
    keys = keyscan_host(host=computer)
    for key in keys:
        key_tracking.append(key)

# Write a new known_hosts file.
print ("keys_to_write:", len(key_tracking))
if key_tracking:

    known_hosts = open(known_host_file, "x")

    for line in key_tracking:
        # print("adding:", line)
        known_hosts.write(line + "\n")

    known_hosts.close()