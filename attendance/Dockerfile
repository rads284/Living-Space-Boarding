FROM python:3.6
COPY requirements.txt /
RUN pip install -r requirements.txt
ADD . /attendance
WORKDIR /attendance
EXPOSE 5000
CMD ["python","attendance.py"]
