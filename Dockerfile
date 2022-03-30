FROM python:3

RUN apt-get update
RUN apt-get install -y wget bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 git mercurial subversion && \
        apt-get clean
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY requirements.txt /usr/src/bot/requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "discordBot.py" ]