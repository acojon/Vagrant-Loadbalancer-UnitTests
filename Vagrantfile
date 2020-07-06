IMAGE_NAME = "generic/debian10"
# NODE_IMAGE_NAME = "generic/debian10"
NODE_IMAGE_NAME = "bento/ubuntu-20.04"
# SWITCH_NAME = "NatNetwork"
# SWITCH_NAME = "Default Switch"
SWITCH_NAME = "External Switch"
# SWITCH_NAME = "WiredEthernet"
NODE_MEMORY = "1024"

N = 2


Vagrant.configure("2") do |config|

  if File.exist?("share.yaml")
    require 'yaml'
    share = YAML::load(File.open("share.yaml"))
  end

  # config.vm.define "dhcp_server" do |dhcp_server|
  #   dhcp_server.vm.box = "jonDHCP"
  #   dhcp_server.vm.hostname = "dhcpserver"
  #   dhcp_server.vm.boot_timeout = 90

  #   dhcp_server.vm.provider "hyperv" do |hv|
  #     hv.vmname = "dhcp_server"
  #     hv.maxmemory = "512"
  #     hv.memory = "512"
  #     hv.cpus = "1"
  #     hv.linked_clone = true

  #     hv.vm_integration_services = {
  #       guest_service_interface: true
  #     }

  #     dhcp_server.vm.synced_folder ".", "/vagrant", smb_username: share['username'], smb_password: share['password']
  #     dhcp_server.vm.network "public_network", bridge: SWITCH_NAME
  #   end

  #   # Import the public key into the authorized_keys, this will let the ansible
  #   # box ssh into the debian box
  #   # dhcp_server.vm.provision "shell", inline: "cat /vagrant/id_rsa.pub >> $HOME/.ssh/authorized_keys", privileged: false
  # end

  (1..N).each do |i|
    config.vm.define "node-#{i}" do |node|
      node.vm.box = NODE_IMAGE_NAME
      node.vm.hostname = "node-#{i}"
      node.vm.boot_timeout = 90

      node.vm.provider "hyperv" do |hv|
        hv.vmname = "node-#{i}"
        hv.maxmemory = NODE_MEMORY
        hv.memory = NODE_MEMORY
        hv.cpus = "1"
        hv.linked_clone = true

        hv.vm_integration_services = {
          guest_service_interface: true
        }

        node.vm.provision "shell", inline: "cat /vagrant/id_rsa.pub >> $HOME/.ssh/authorized_keys", privileged: false
        node.vm.synced_folder ".", "/vagrant", smb_username: share['username'], smb_password: share['password']
        node.vm.network "public_network", bridge: SWITCH_NAME
      end
    end
  end

  config.vm.define "lb" do |lb|
    lb.vm.box = NODE_IMAGE_NAME
    lb.vm.hostname = "lb"

    # Import the public key into the authorized_keys, this will let the ansible
    # box ssh into the debian box
    lb.vm.provision "shell", inline: "cat /vagrant/id_rsa.pub >> $HOME/.ssh/authorized_keys", privileged: false

    lb.vm.provider "hyperv" do |hv|
      hv.vmname = "lb"
      hv.maxmemory = NODE_MEMORY
      hv.memory = NODE_MEMORY
      hv.cpus = "1"
      hv.linked_clone = true

      lb.vm.provision "shell", inline: "cat /vagrant/id_rsa.pub >> $HOME/.ssh/authorized_keys", privileged: false
      lb.vm.synced_folder ".", "/vagrant", smb_username: share['username'], smb_password: share['password']
      lb.vm.network "public_network", bridge: SWITCH_NAME
    end
  end

  config.vm.define "testing" do |testing|
    testing.vm.box = NODE_IMAGE_NAME
    testing.vm.hostname = "testing"

    # Import the public key into the authorized_keys, this will let the ansible
    # box ssh into the debian box
    testing.vm.provision "shell", inline: "cat /vagrant/id_rsa.pub >> $HOME/.ssh/authorized_keys", privileged: false

    testing.vm.provider "hyperv" do |hv|
      hv.vmname = "testing"
      hv.maxmemory = NODE_MEMORY
      hv.memory = NODE_MEMORY
      hv.cpus = "1"
      hv.linked_clone = true

      testing.vm.provision "shell", inline: "cat /vagrant/id_rsa.pub >> $HOME/.ssh/authorized_keys", privileged: false
      testing.vm.synced_folder ".", "/vagrant", smb_username: share['username'], smb_password: share['password']
      testing.vm.synced_folder "example_tests", "/home/vagrant/example_tests", smb_username: share['username'], smb_password: share['password']
      testing.vm.synced_folder "http_tests", "/home/vagrant/http_tests", smb_username: share['username'], smb_password: share['password']
      testing.vm.synced_folder "https_tests", "/home/vagrant/https_tests", smb_username: share['username'], smb_password: share['password']
      testing.vm.network "public_network", bridge: SWITCH_NAME
    end

    # Copy the public key 
    testing.vm.provision "file", source: "id_rsa.pub", destination: ".ssh/id_rsa.pub"

    # Copy the private key
    testing.vm.provision "file", source: "id_rsa", destination: ".ssh/id_rsa"

    # Set the permissions appropriately for the private key
    testing.vm.provision "shell", inline: "chmod 600 $HOME/.ssh/id_rsa", privileged: false
  end

  config.vm.define "ansible", primary: true do |ansible|
    ansible.vm.box = "jonAnsible"
    ansible.vm.hostname = "ansible"

    ansible.vm.provider "hyperv" do |hv|
      hv.vmname = "ansible"
      hv.memory = "2048"
      hv.linked_clone = true

      ansible.vm.synced_folder ".", "/vagrant", smb_username: share['username'], smb_password: share['password']

      # This folder contains the ansible plays :)
      ansible.vm.synced_folder "HTTPPlaybooks", "/home/vagrant/ansible", smb_username: share['username'], smb_password: share['password']
      ansible.vm.synced_folder "HTTPSPlaybooks", "/home/vagrant/HTTPSPlaybooks", smb_username: share['username'], smb_password: share['password']

      ansible.vm.network "public_network", bridge: SWITCH_NAME
    end

    ansible.vm.provision :host_shell do |host_shell|
      host_shell.inline = "powershell -c ./GetIPAddresses.ps1"
    end

    # ansible.vm.provision :host_shell do |host_shell|
    #   host_shell.inline = "powershell -c ./SetFixedMACAddress.ps1"
    # end

    # # ansible.vm.provision :host_shell do |host_shell|
    # #   host_shell.inline = "powershell -c ./SetVMBandwidthLimit.ps1"
    # # end

    # # Disable while troubleshooting flannel
    # ansible.vm.provision :host_shell do |host_shell|
    #   host_shell.inline = "powershell -c ./SetMacAddressSpoofing.ps1"
    # end

    # Update the local hosts file with the name/ip address for the other computers
    ansible.vm.provision "shell", inline: "python3 /vagrant/hosts.py", privileged: true

    # Update the local hosts file with the name/ip address for the other computers
    ansible.vm.provision "shell", inline: "python3 /vagrant/keys.py", privileged: false

    # Copy the public key 
    ansible.vm.provision "file", source: "id_rsa.pub", destination: ".ssh/id_rsa.pub"

    # Copy the private key
    ansible.vm.provision "file", source: "id_rsa", destination: ".ssh/id_rsa"

    # Set the permissions appropriately for the private key
    ansible.vm.provision "shell", inline: "chmod 600 $HOME/.ssh/id_rsa", privileged: false

    # Copy the Ansible Vault key
    ansible.vm.provision "file", source: ".ansible_keys", destination: "$HOME/.ansible_keys"

    ansible.vm.provision "shell", path: "ansible.sh", privileged: false
  end
end