FROM python:3.11-alpine

WORKDIR /app
COPY main.py main.py
COPY conf.py conf.py
COPY rename.py rename.py
COPY tree.py tree.py
COPY watcher.py watcher.py
RUN pip3 install --no-cache-dir watchdog
COPY commond.sh /bin/aninamer
RUN mkdir -p /app/video

CMD ["aninamer","start"]