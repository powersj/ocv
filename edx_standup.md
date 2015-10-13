#edX Platform Standup Instructions

## Introduction
The following is meant to be instructions on what was required to build the edX development platform in my own enviornment. The development enviornment consists of two main parts:

  * LMS - The student facing website
  * Studio - the course authoring software

These instructions will setup both. There is a third part, for the discussion forums, however these are of no interest to this project.

## Pre-Reqs
The edX platform uses an existing vagrant image that works along side Virutal Box. Therefore, both virutal box and vagrant are required to be installed on the system being used for development.

You also will need the nfs-kernel-server package to allow for NFS mounting the images.

These can all be obtained simply by running the following on a Debian/Ubuntu system:
```
# apt update
# apt install vagrant virtualbox nfs-kernel-server
```

## Bring-up
Begin by reviewing the official instructions found here:
https://github.com/edx/configuration/wiki/edX-Developer-Stack#installing-the-edx-developer-stack

These will give a very simple and easy to use steps. For example, all the author had to complete were these five commands. This whole process will take 10-15mins. depending on the internet connection.

1. mkdir devstack
2. cd devstack
3. curl -L https://raw.githubusercontent.com/edx/configuration/master/vagrant/release/devstack/Vagrantfile > Vagrantfile
4. vagrant plugin install vagrant-vbguest
5. vagrant up

At this point the vagrant image is up and running and will begin to boot. Once booted it will update and load the latest bits on the system, including getting all necessary dependencies.

## LMS App
- Login to the VM
```
# vagrant up and vagrant ssh
```

- Use the edxapp account
```
# sudo su edxapp
```

- Start the LMS app: 
```
# paver devstack lms
```

- View the app at:
```
# http://localhost:8000/
```

- Finally, if speed is required and you do not wish to update the envionrment then when starting run:
```
# paver devstack --fast lms
```

## Studio App
- Login to the VM
```
# vagrant up and vagrant ssh
```

- Use the edxapp account
```
# sudo su edxapp
```

- Start the LMS app: 
```
# paver devstack studio
```

- View the app at:
```
# http://localhost:8001/
```

- Finally, if speed is required and you do not wish to update the envionrment then when starting run:
```
# paver devstack --fast studio
```


## Development
At this point the system is ready for development purposes. For more information see:
https://github.com/edx/edx-platform/wiki/Developing-on-the-edX-Developer-Stack

## Troubleshooting
If you run into issues with vagrant, bring up virtual box and watch the VM system boot up. In doing so you have more information being provided by the VM to you and can make a determiniation as to what a possible problem might be (assuming you run into one).
