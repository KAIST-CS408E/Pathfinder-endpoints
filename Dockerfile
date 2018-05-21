FROM python:3.6
LABEL maintainer="seokchan.ahn@kaist.ac.kr"

WORKDIR /workspace
ADD requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
