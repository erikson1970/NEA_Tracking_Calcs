# Remote Dev Container Builder
#   credit to Youtube's @Astroniz for original and inspiration
#
FROM python:3.9-buster

LABEL description="Remote Container Builder"
LABEL version="0.2"

ARG username=nonrootuser

RUN apt-get update && apt-get -y install apt-utils sudo openssh-client curl git
RUN adduser --disabled-password --gecos "" $username
RUN usermod -a -G sudo $username
#this hash is the result of "echo [USERNAME]:$(openssl passwd -5 -salt $RANDOM  [yourpassword]) | base64 -w 0"
#eg:  input:  echo nonrootuser:$(openssl passwd -5 -salt $RANDOM  monkey1234) | base64 -w 0
#    output: bm9ucm9vdHVzZXI6JDUkMTE3NDQkNjNPSzJmMGRLcXA1VE5UNFRpQ01sYjlVWEpxZFNuOWJaN3ByOTBWNzcxOAo=
RUN echo bm9ucm9vdHVzZXI6JDUkMTE3NDQkNjNPSzJmMGRLcXA1VE5UNFRpQ01sYjlVWEpxZFNuOWJaN3ByOTBWNzcxOAo= | base64 -d | chpasswd -e
USER $username
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-warn-script-location --no-cache-dir -r requirements.txt
## uncomment next line if you want to start the container as root.
#USER root
#
ENV PYTHONPATH "/"

WORKDIR /.