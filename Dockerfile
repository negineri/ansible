FROM python:3
ARG VERSION
RUN pip install ansible==${VERSION}
