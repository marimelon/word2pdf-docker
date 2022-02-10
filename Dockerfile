FROM python:3.10-slim-bullseye

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -qq \
    && apt-get install -y -q libreoffice fonts-noto-cjk \
    && apt-get remove -y -q libreoffice-gnome

RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/apt/archives/*.deb /var/cache/apt/*cache.bin

RUN pip install fastapi uvicorn python-multipart

WORKDIR /work
COPY ./main.py /work/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
