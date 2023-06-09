FROM python:3.11-buster
ENV PYTHONUNBUFFERED True

WORKDIR /app
COPY . .

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-dev libglib2.0-0 libsm6 libxrender1 libxext6
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# m1対応
RUN apt-get install -y wget bash git gcc g++ gfortran  liblapack-dev libamd2 libcholmod3 libmetis-dev libsuitesparse-dev libnauty2-dev
RUN wget -nH https://raw.githubusercontent.com/coin-or/coinbrew/master/coinbrew
RUN chmod u+x coinbrew
RUN bash coinbrew fetch Cbc@master
RUN bash coinbrew build Cbc@master --no-prompt --prefix=/usr/local --tests=none --enable-cbc-parallel
ENV PMIP_CBC_LIBRARY="/usr/local/lib/libCbc.so"
ENV LD_LIBRARY_PATH="/home/haroldo/prog/lib"


ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]