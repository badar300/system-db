# base image  
FROM python:3.9

# set work directory  
RUN mkdir -p /home/app
WORKDIR /home/app/
RUN git clone https://x-token-auth:ATCTT3xFfGN0YrIc9E33mw95XCdYqtoAQekrkA5iCvSXWTmVZZqoevaJDoZrwvj-EGVWjZv2KRcQNiM7XN5lDrTT5wlprpm6ul_pS_9ABVcT6_hHKK4AcJ8C55jY5ULBsl0rwW1P-df7aenLdCALKozrNBozAWn6nek1ZeL0bXiDGZRh6M-7lJ0=79509207@bitbucket.org/raymonde_haynes/sysdb.git

# where your code get run from
WORKDIR /home/app/sysdb 

# # set environment variables  
# # ENV PYTHONDONTWRITEBYTECODE 1
# # ENV PYTHONUNBUFFERED 1  

# # install dependencies  
RUN pip install --upgrade pip  
RUN pip install -r requirements.txt  

# # start server  
# # WORKDIR /home/app/dj_docker_drf
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000

# Build docker file then run it
# docker rm -f system_db 
# docker build -t system_db . 
# docker run --name system_db -di -p 0.0.0.0:8000:8000 system_db 