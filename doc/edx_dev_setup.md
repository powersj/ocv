#edX Development Platform Setup

## Introduction
The following is meant to be instructions on what was required to build the edX development
platform in my own environment. The development environment consists of two main parts:

  * LMS - The student facing website
  * Studio - the course authoring software

These instructions will setup both. There is a third part, for the discussion forums, however these
are of no interest to this project.

## Pre-Reqs
The edX platform uses an existing vagrant image that works along side Virtual Box. Therefore, both
virtual box and vagrant are required to be installed on the system being used for development.

You also will need the nfs-kernel-server package to allow for NFS mounting the images.

These can all be obtained simply by running the following on a Debian/Ubuntu system:
```bash
# apt update
# apt install vagrant virtualbox nfs-kernel-server
```

## Bring-up
Begin by reviewing the official instructions found here:
https://github.com/edx/configuration/wiki/edX-Developer-Stack#installing-the-edx-developer-stack

These will give a very simple and easy to use steps. For example, all the author had to complete
were these five commands. This whole process will take 10-15mins. depending on the Internet
connection.

```bash
# mkdir devstack && cd devstack
# curl -L https://raw.githubusercontent.com/edx/configuration/master/vagrant/release/devstack/Vagrantfile > Vagrantfile
# vagrant plugin install vagrant-vbguest
# vagrant up
```

At this point the vagrant image is up and running and will begin to boot. Once booted it will
update and load the latest bits on the system, including getting all necessary dependencies.

## LMS App
To start the LMS application the following steps are required:

- Login to the VM
- Change over to the edxapp account
- Start the LMS app:
- View the app at the correct port

This is accomplished via the following commands:
```bash
# vagrant up and vagrant ssh
# sudo su edxapp
# paver devstack lms
# http://localhost:8000/
```

Finally, if speed is required and you do not wish to update the environment then when starting
run the paver command with --fast option, as such:
```bash
# paver devstack --fast lms
```

## Studio App
To start the studio application the following steps are required:

- Login to the VM
- Use the edxapp account
- Start the Studio app:
- View the app at the correct port

This is accomplished via the following commands:
```bash
# vagrant up and vagrant ssh
# sudo su edxapp
# paver devstack studio
# http://localhost:8001/
```

Finally, if speed is required and you do not wish to update the environment then when starting
run the paver command with --fast option, as such:
```bash
# paver devstack --fast studio
```

## Development
At this point the system is ready for development purposes. For more information see:
https://github.com/edx/edx-platform/wiki/Developing-on-the-edX-Developer-Stack

## Troubleshooting
If you run into issues with vagrant, bring up virtual box and watch the VM system boot up. In
doing so you have more information being provided by the VM to you and can make a determination
as to what a possible problem might be (assuming you run into one).

### MongoDB Conn Error 111
If you get the following MongoDB error message:
```
pymongo.errors.ConnectionFailure: [Errno 111] Connection refused
```

Run the following set of commands:
```bash
# sudo rm /edx/var/mongo/mongodb/mongod.lock
# sudo -u mongodb mongod --dbpath /edx/var/mongo/mongodb --repair --repairpath /edx/var/mongo/mongodb
# sudo start mongod
```

Then mongod process will be running as expected and you can start the services successfully.
