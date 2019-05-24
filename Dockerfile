FROM python:2.7-slim

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

ENV NAME Article_splicing

CMD ["python", "file_split_and_splicing.py"]
