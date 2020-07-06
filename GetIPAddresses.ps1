<#
Problem: How to communicate the ip addresses for Node-1, Node-2 and lb to the
various vagrant boxes in the vagrant file when they're booted?

HyperV doesn't have a lot of support for network configuration via Vagrant. I
can't set static IP addresses on the vagrant boxes, they just pick a random ip
in the 192.168.0.0 vlan.  There is already a hosts.ini file in the repository,
the file is used by a couple python scripts to set the hosts file, set ip
addresses, etc.  By running this script, the hosts.ini file is updated with the
IP address values as retrieved from Hyperv.
#>
$ErrorActionPreference = "stop"
Set-StrictMode -Version Latest

$IniFile = ".\hosts.ini"

$vms = get-vm

$data = @()
foreach ($vm in $vms) {
    try {
        $vm.NetworkAdapters.IPAddresses | Out-Null
    }
    catch {
        continue
    }
    write-host $vm.name
    $line = ""
    $line += "["
    $line += $vm.Name
    $line += "]"
    $data += $line
    $data += "entry_type = ipv4"
    
    # Sometimes an IPv6 address is returned along with the IPv4 address.  This
    # will filter out the IPv6 addresses.
    $IPAddresses = $vm.NetworkAdapters.IPAddresses -split ","
    $address = ""
    foreach ($ip in $IPAddresses) {
        $temp = [System.Net.IPAddress] $ip
        if (-not ($temp.IsIPv6LinkLocal)) {
            $address = $temp.IPAddressToString
        }
    }

    $line = ""
    $line += "address = "
    $line += $address
    $data += $line

    $line = ""
    $line += "names="
    $line += $vm.Name
    $data += $line

    $data += ""
}

$line = ""
$line += "[gitlab]"
$data += $line

$data += "entry_type = ipv4"
$data += "address = 10.0.0.56"
$data += "names=gitlab"
$data += ""

$data | Set-Content -Path $IniFile 