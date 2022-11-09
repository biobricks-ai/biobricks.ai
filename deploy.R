#!/bin/sh
pacman::p_load(paws, tidypaws, tidyverse)

ec2 = paws::ec2()

# CREATE VOLUME with 100gb
res = ec2$describe_volumes() |> tidypaws() |> pluck("Volumes")
vol = ec2$create_volume(AvailabilityZone="us-east-1e",VolumeType="gp3",
  TagSpecifications=list(list(ResourceType="volume",Tags=list(list(Key="Name",Value="biobricks")))),
  Iops=3000L, Size=100L)

# CREATE INSTANCE
block_devices = list(list(DeviceName="/dev/sdh",Ebs=list(VolumeSize=100L)))

instances = ec2$run_instances(
  KeyName="biobricks",
  BlockDeviceMappings=block_devices,
  ImageId="ami-0149b2da6ceec4bb0", 
  TagSpecifications=list(list(ResourceType="instance",Tags=list(list(Key="Name",Value="biobricks")))),
  MaxCount=1, MinCount=1, InstanceType="t2.small", SecurityGroupIds=list("sg-0ca47685c1c1beb6e"),
  Placement = list(AvailabilityZone = "us-east-1e"))

instance = instances$Instances[[1]]
Sys.sleep(30)

## Attach volume
att_vol = ec2$attach_volume(Device="/dev/sdd", InstanceId = instance$InstanceId, VolumeId=vol$VolumeId)
print(att_vol)

## Associate IP
ass_eip = ec2$associate_address(AllocationId="eipalloc-0eb3fa8acfe897546",InstanceId=instance$InstanceId)

## Point route53
# TODO

# ssh -i ~/.ssh/biobricks ubuntu@ec2-18-233-246-97.compute-1.amazonaws.com

## GET DOCKER AND DOCKER COMPOSE
# sudo apt update
# sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
# sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
# apt-cache policy docker-ce
# sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
# sudo groupadd docker
# sudo usermod -aG docker ubuntu

## AWS CLI
# sudo apt install aws-cli

## Upload docker-compose.yml
# scp -i ~/.ssh/biobricks ./docker-compose.yml ubuntu@ec2-18-233-246-97.compute-1.amazonaws.com:/home/ubuntu/docker-compose.yml

## AWS ECR login
# aws ecr get-login-password --region us-east-1 | \
  # docker login --username AWS --password-stdin \
  # 951523641836.dkr.ecr.us-east-1.amazonaws.com/bbportal

## NGINX
# sudo apt install nginx
# sudo ufw allow 'Nginx HTTP'
# sudo ufw allow ssh
# sudo ufw status

## ADD THE BELOW TO /etc/nginx/sites-enabled/default
# location / {
#   proxy_pass  http://0.0.0.0:5000;
#   proxy_set_header Host $host;
#   proxy_set_header X-Real-IP $remote_addr;
#   proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
# }

# docker compose pull
# docker compose up
