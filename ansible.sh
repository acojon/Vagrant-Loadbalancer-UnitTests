cd /home/vagrant/ansible

ssh-add

eval $(ssh-agent -s)
ssh-add ../.ssh/id_rsa
ssh-add -l

ansible-galaxy install -r roles/requirements.yaml -p ./roles

ansible-playbook -i production.yaml site.yaml --vault-password-file ../.ansible_keys/VaultPassword
