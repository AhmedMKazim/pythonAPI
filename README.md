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
15- create requirement file contain all package used execute
  pip freeze # to show all pakages use by the project
  then execute
  pip freeze > requirements.txt # to add all packages to this file
16- go to models.py and adding this
`    from django.db import models
    from django.contrib.auth.models import AbstractBaseUser
    from django.contrib.auth.models import PermissionsMixin
    from django.contrib.auth.models import BaseUserManager

    class UserProfileManager(BaseUserManager):
        """Help django work with our custom user model."""

        def create_user(self, email, name, password=None):
            """Creates a new user profile object."""
            if not email:
                raise ValueError('Users must have an email address.')
            email = self.normalize_email(email) # make all char lowercase
            user = self.model(email=email, name=name) # create new user object

            user.set_password(password) # will incript password
            user.save(using=self._db)
            return user

        def create_superuser(self, email, name, password):
            """Creates and saves a new superuser with given details."""

            user = self.create_user(email, name, password)

            user.is_superuser = True
            user.is_staff = True

            user.save(using=self._db)

            return user


    class UserProfile(AbstractBaseUser, PermissionsMixin): # inherited from AbstracktBaseUser, PermissionsMixin
        """Respents a "user profile" inside our system."""
        email = models.EmailField(max_length=255, unique=True)
        name = models.CharField(max_length=255)
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=False)
        objects = UserProfileManager()
        USERNAME_FIELD = 'email' # is already required by the system
        REQUIRED_FIELDS = ['name']

        def get_full_name(self):
            """Used to get a users full name."""
            return self.name

        def get_short_name(self):
            """Used to get a users short name."""
            return self.name
        def __str__(self):
            """Django uses this when it needs to convert the object to a string"""
            return self.email`
    to create user model

17- make django use our custom user model by going to settings.py and add this line in the last
  AUTH_USER_MODEL = 'pythonApi.UserProfile'
