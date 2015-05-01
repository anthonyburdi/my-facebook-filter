# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  # To run on your local machine:
  config.vm.provider :virtualbox do |provider|
    config.vm.box = "ubuntu/trusty64"
    config.vm.network "forwarded_port", guest: 5001, host: 5001
  end

  # To run on Amazon AWS
  config.vm.provider :aws do |provider, override|
    # You can create access keys via the Amazon AWS dashboard, the code
    # below assumes you store these values on your development machine
    # as environment variables
    provider.access_key_id = ENV["AWS_ACCESS_KEY"]
    provider.secret_access_key = ENV["AWS_SECRET_KEY"]
    provider.keypair_name = ENV["AWS_KEYPAIR_NAME"]
    provider.security_groups = [ENV["AWS_SECURITY_GROUP"]]
    provider.subnet_id = ENV["AWS_PROVIDER_ID"]

    # Set the type of instance:
    provider.instance_type = "t2.micro"
    # Ubuntu Server 14.04 LTS (HVM), SSD Volume Type - ami-d05e75b8
    provider.ami = "ami-d05e75b8"
    provider.region = "us-east-1"

    # Set the private key so you can connect to the instance (see AWS docs)
    override.vm.box = "dummy"
    override.ssh.username = "ubuntu"
    override.ssh.private_key_path = ENV["AWS_KEYPAIR_PRIVATEKEY_PATH"]
  end

  # Run the provisioning script to install dependencies
  config.vm.provision :shell, path: "provision.sh"

end
