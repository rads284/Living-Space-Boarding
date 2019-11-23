FROM alpine:3.7

RUN apk add --update py-pip


#ADD requirements.txt /SE_Project/

# Set the working directory to /SE_Project
WORKDIR /SE_Project
RUN apk add --update python py-pip
# Install app dependencies
RUN pip install Flask
RUN pip install flask-mail
RUN pip install -U flask-cors
RUN pip install requests
#RUN pip install -r requirements.txt


# Bundle app source
COPY . /SE_Project

EXPOSE  80
# Define environment variable



CMD ["python", "leave_management.py"]