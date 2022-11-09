
# How was this set up?
Using instructions at [1].

1. `eb init` init elastic beanstalk
2. `aws ecr create-repository --repository-name bbportal` create bbportal ecr
3. aws ecr login
```
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  951523641836.dkr.ecr.us-east-1.amazonaws.com/bbportal
```
4. `docker compose push` --- push to bbportal ECR
5. `eb create biobricks-env` create ebs environment  

## How to tear down?
`eb terminate`

# references
1. https://medium.com/adessoturkey/aws-elastic-beanstalk-with-docker-compose-yml-file-ae5958569b2f