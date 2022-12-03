# deployment

1. make code changes
2. ecr login
3. docker build -t 951523641836.dkr.ecr.us-east-1.amazonaws.com/bbportal:latest .
4. docker push 951523641836.dkr.ecr.us-east-1.amazonaws.com/bbportal:latest
5. scp docker-compose.yml biobricks.ai:/home/ubuntu/docker-compose.yml
6. ssh biobricks.ai
7. screen -r biobricks
8. 