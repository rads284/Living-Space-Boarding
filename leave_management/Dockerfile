FROM python:3.6
COPY requirements.txt /
RUN pip install -r requirements.txt
# Bundle app source
COPY . /leave
WORKDIR /leave
EXPOSE  8000
# Define environment variable
CMD ["python", "leave_management.py"]