FROM python:3.8-slim-buster

RUN apt-get update && \
    apt-get install -y gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" 

RUN mkdir chrome \
    && unzip /chromedriver/chromedriver* -d /usr/src/chrome \
    && apt-get remove -y unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./usr/src/

CMD [ "python", "movie_review_crawler.py" ]


# docker build --platform linux/amd64 -t review_crawler .