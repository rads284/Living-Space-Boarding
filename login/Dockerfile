FROM python:3.6
COPY requirements.txt /
RUN pip install -r requirements.txt
ADD . /registration
WORKDIR /registration
EXPOSE 8000
CMD ["python","login.py"]