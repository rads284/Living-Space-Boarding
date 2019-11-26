FROM python:3.6
COPY requirements.txt /
RUN pip install -r requirements.txt
ADD . /otp
WORKDIR /otp
EXPOSE 8000
CMD ["python","otp.py"]