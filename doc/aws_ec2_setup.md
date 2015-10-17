# Amazon EC2 Setup
## Introduction
This file states the setup and configuration details of the Amazon EC2 instance. This instance will
be used for demo purposes of the visualization and to allow anyone from around the world to see.

## Setup
For this I used my personal Georgia Tech email address to create a free AWS account. I have created
a single mini free instance as well.

## Connecting
To connect via SSH, you need the SSH key that was generated and then find the IP address from the
Amazon console. Then you can run:

```shell
ssh -i ~/.ssh/aws-key.pem ubuntu@IP_ADDRESS
```

The ubuntu user has sudo permissions.

At this point the user can setup whatever is required.
