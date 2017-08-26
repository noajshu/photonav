FROM python:3.6
WORKDIR /root/
ADD code/requirements.txt ./
RUN pip install -r requirements.txt
ADD code/ ./
CMD python app.py