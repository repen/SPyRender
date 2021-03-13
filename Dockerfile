#docker build -t build_name:latest .
#docker run --name container_name -d build_name:latest
#docker run --name container_name -d -p 8120:5000 build_name:latest
#docker run --name container_name -d -v volume:/script/data -p 8120:5000 build_name:latest
FROM python:3.8


# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99


ENV BASE_DIR /script
ENV EXTERNAL_WORK true
ENV REMOTE_SERVER None

WORKDIR ${BASE_DIR}

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY script ${BASE_DIR}

#CMD python main.py
CMD tail -f /dev/null