# Python Restfull api
this app providing basic functionality for managing user profiles.

1 - create gitignore files

2 - create vagrant file by
  `vagrant init`
3 - replace vagrantfile content with
  `# -*- mode: ruby -*-
  # vi: set ft=ruby :

  # All Vagrant configuration is done below. The "2" in Vagrant.configure
  # configures the configuration version (we support older styles for
  # backwards compatibility). Please don't change it unless you know what
  # you're doing.
  Vagrant.configure("2") do |config|
    # The most common configuration options are documented and commented below.
    # For a complete reference, please see the online documentation at
    # https://docs.vagrantup.com.

    # Every Vagrant development environment requires a box. You can search for
    # boxes at https://atlas.hashicorp.com/search.
    config.vm.box = "ubuntu/xenial64"

    config.vm.network "forwarded_port", host_ip: "127.0.0.1", guest: 8080, host: 8080

    config.vm.provision "shell", inline: <<-SHELL
      # Update and upgrade the server packages.
      sudo apt-get update
      sudo apt-get -y upgrade
      # Set Ubuntu Language
      sudo locale-gen en_GB.UTF-8
      # Install Python, SQLite and pip
      sudo apt-get install -y python3-dev python-pip sqlite
      # Upgrade pip to the latest version.
      sudo pip install --upgrade pip
      # Install and configure python virtualenvwrapper.
      sudo pip install virtualenvwrapper
      if ! grep -q VIRTUALENV_ALREADY_ADDED /home/vagrant/.bashrc; then
          echo "# VIRTUALENV_ALREADY_ADDED" >> /home/vagrant/.bashrc
          echo "WORKON_HOME=~/.virtualenvs" >> /home/vagrant/.bashrc
          echo "PROJECT_HOME=/vagrant" >> /home/vagrant/.bashrc
          echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
      fi
    SHELL

  end`

4 - then execute vagrant up to start download files
5 - to inter vagrant machine
  `vagrant up`
  `vagrant ssh`
  and using `exit` to exit from machine
6 - then create virtual environments
  `mkvirtualenv pythonApi --python=python3
`
a problem was occures in this line and I didn't found it's solve!

7- install packages
    pip install django # he use 1.11 and I use latest => 2.2.12
    pip install djangorestframework
8- create src folder in your main directory
9- redirect in vagrant machine to vagrant folder then to src folder
10- execute
  django-admin.py startproject profiles_project to create new project
11- then redirect in vagrant machine to vagrant/src/profiles_project and execute
  python manage.py startapp pythonApi # to create

Note: profiles_project contain setting of all PROJECT_HOME

12- go to settings.py inside profiles_project and enable djangorestframework by adding new line in INSTALLED_APPS array
  'rest_framework'
13- then add 'rest_framework.authtoken' to same array
14- then also add 'pythonApi' to same array
Note: when add any extra app you should add it to this array and if not it will never working
