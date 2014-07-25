# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "trusty64"
  config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
  config.vm.hostname = "nyc-inspections"
  config.vm.network "private_network", ip: "88.88.88.88"

  config.vm.synced_folder "nyc_inspections", "/home/nyc_inspections/apps/nyc_inspections"

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "provisioning/ansible/playbook.yml"
    ansible.extra_vars = "provisioning/ansible/defaults/main.yml"
  end
end
