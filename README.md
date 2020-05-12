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
18- then create migration by execute
  `python manage.py makemigrations`
19- then do migrate by execute
  `python manage.py migrate # by this db.sqlite3 file will created contain all tables`
20- now you can create your admin acount by execute
   `python manage.py createsuperuser # and fill data of user`
21- to register user admin change admin.py inside pythonApi file content to
  `from django.contrib import admin

  from . import models

  admin.site.register(models.UserProfile)`
22- now we can test admin users first execute
  `python manage.py runserver 0.0.0.0:8080`
  then access to admin panel by http://127.0.0.1:8080/admin/
  login using you superuser details and enter to the panel
23- create test APIView by going to views.py in our applicatin pythonApi
24- you can add new url inside profiles_project in urls.py file and we will create urls for each application
to create urls file to pythonApi applicatin first add this import to include
`from django.conf.urls import include`
and in urlpatterns array add this item
  `path('api/', include('pythonApi.urls'))`
then create urls file in pythonApi
put inside it
  ` from django.urls import path
    from . import views
    urlpatterns = [
        path('hellow-view/', views.HellowApiView.as_view())
    ]`

25- create serializers file and put inside it
    `from rest_framework import serializers
    class HelloSerializer(serializers.Serializer):
    """Serializers a name field for testing ou APIView"""
    name = serializers.CharField(max_length=10)`

26- import these to use them
    `from  rest_framework import status
    from . import serializers`
    and after class declration add
    `serializer_class = serializers.HelloSerializer; # describe the serializer`

27- create post method
      `def post(self, request):
        """ Create a hellow message with our nme."""
        serializer = serializer.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )`
28- create put patch and delete method by adding these lines
`    def put(self, request, pk=None):
        """Handles updating an object."""

        return Response({'method': 'put'})
    def patch(self, request, pk=None):
        """Patch request, only updates fields provided in the request."""
        return Response({'method': 'patch'})
    def delete(self, request, pk=None):
        """Deletes and object."""
        return Response({'method': 'delete'})
`
29- now we will create ViewSet
  import it inside views.py
    `from rest_framework import viewsets`
and below old class in views.py create viewset class and add list to list all items as shown below
    `class HelloViewSet(viewsets.ViewSet):
    def list(self, request):
        """Return a hello message."""
        an_viewset = [
            'Uses HTTP methods as functin (get, post, patch, put, delete)',
            'It is similar to a traditional Django view',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello!', 'an_viewset': an_viewset})`
30- add url router add these line to urls.py which created in pythonApi
  `from django.conf.urls import include
  from rest_framework.routers import DefaultRouter

  router =  DefaultRouter()
  router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')`
  and inside urlpatterns array add this items
  `path('', include(router.urls))`
31- Add create, retrieve, update, partial update and destroy functions by adding these functions inside class which created below list functoin
        `def create(self, request):
          """Create a new hello message."""
          serializer = serializers.helloserializer(data=request.data)
          if serializer.is_valid():
              name = serializer.data.get('name')
              message = 'Hello {0}'.format(name)
              return Response({'messge': message})
          else:
              return Response(
                  serializer.errors, status=status.HTTP_400_BAD_REQUEST
              )
        def retrieve(self, request, pk=None):
            """Handles getting an object by its ID."""
            return Response({'http_method': 'GET'})
        def update(self, request, pk=None):
            """Handles updating an object."""
        def partial_update(self, request, pk= None):
            """Handles updating part of an object."""
            return Response({'http_method': 'PATCH'})
        def destroy(self, request, pk=None):
            """Handles removing an object."""
            return Response({'http_method': 'DELETE'})`


32- Create user profile serializer in serializers.py inside pythonApi folder
  first import models by
  `from . import models`
  then add this class
  `class UserProfileSerializer(serializers.ModelSerializer):
      """A serializer for our user profile objects."""

      class Meta: # to tell djangorestframework what is the model
          model = models.UserProfile
          fields = ('id', 'email', 'name', 'password')
          extra_kwargs = {'password': {'write_only': True}}

      def create(self, validated_data):
          """Create and return a new user."""

          user = models.UserProfile(
              email=validated_data['email'],
              name=validated_data['name']
          )

          user.set_password(validated_data['password'])
          user.save()

          return user`
33- Create profiles ViewSet
    first import model by
    `from . import models`
    then add this class
    `class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, ceating and updating profiles."""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()`

34- Register profile ViewSet with the URL router by adding this line below old router in urls.py
  `router.register('profile', views.UserProfileViewSet) # when using model you don't need to add basename its taked from the model`
35- Create permission class
  first of all create permission.py file, here will store all permissions
  then fill it with
  `class UpdateOwnProfile(permissions.BasePermission):
      """Allow users to edit their own profile."""
      def has_object_permission(self, request, view, obj):
          """Check user is trying to edit their own profile."""
          if request.method in permissions.SAFE_METHODS: # if user the method is get only
              return True
          # here if obj data is updated
          return obj.id == request.user.id # obj is the object which edited by the user`
36- Add authentication and permissions to ViewSet
  start by addding
  `from . import permissions`
  then inside UserProfileViewSet adding in last lines
  ` authentication_classes = (TokenAuthentication,) # , = tuple: mean that this is imutable which mean it can not be change after set
    permission_classes = (permissions.UpdateOwnProfile,)`
37- Add search profiles feature
    first in view.py
    `from rest_framework import filters`
    and in the last add
    ` filter_backends = (filters.SearchFilter,)
      search_fields = ('name', 'email',) #felters by name or email`
38- Create login API ViewSet in view.py add
  ` from rest_framework.authtoken.serializers import AuthTokenSerializer
    from rest_framework.authtoken.views import ObtainAuthToken`
    and in the last add
    `class LoginVieSet(viewsets.ViewSet):
        """Checks email and password and return an auth token."""
        serializer_class = AuthTokenSerializer

        def create(self, request): # post function
            """Use the ObtainAuthToken APIView to validate and create a tookeno."""

            return ObtainAuthToken().post(request)`

    and in urls.py add the router
    `router.register('login', views.LoginVieSet, basename='login')`
