#__author__ = "David J. Alouani, david.alouani@uhhospitals.org, david.j.alouani@gmail.com"
#__date__ = "January 1, 2021 10:00:00 AM"
# qPCRdeepNet

FROM ubuntu:16.04

RUN apt-get update && apt-get upgrade\
     && apt-get -y install vim wget python-pip\
    && wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh\
    && mkdir /root/.conda\
    && bash Miniconda3-latest-Linux-x86_64.sh -b\
    && rm -f Miniconda3-latest-Linux-x86_64.sh

ENV PATH="/root/miniconda3/bin:${PATH}"
RUN conda install -y -c conda-forge keras && pip install pandas Pillow matplotlib scipy

RUN pip install tensorflow

COPY qpcrdeepnet /home/qpcrdeepnet

ADD runai.sh /
RUN chmod +x /runai.sh
CMD ["/runai.sh"]
