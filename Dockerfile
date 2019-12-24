FROM python:3.7.5
ENV PYTHONUNBUFFERED 1

# Upgrade pip before installing packages
RUN pip install --upgrade --no-cache-dir pip

COPY requirements.txt /home/docker/code/
RUN pip install -r /home/docker/code/requirements.txt
