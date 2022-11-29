FROM mongo
WORKDIR /MongoDB_Flask_Heroku
COPY . /MongoDB_Flask_Heroku
RUN set -xe \
    && apt-get update -y \
    && apt-get install -y python3-pip \
    && apt-get install -y python3.7 \ 
    && apt install -y vim
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
