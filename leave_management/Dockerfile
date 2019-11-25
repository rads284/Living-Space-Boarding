FROM python:3.6
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY . /leave
WORKDIR /leave
EXPOSE  8000
CMD ["python", "leave_management.py"]