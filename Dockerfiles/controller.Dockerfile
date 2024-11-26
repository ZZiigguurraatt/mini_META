# 24.04 requires pip3 to use --break-system-packages and then the build fails.... need to investigate
FROM ubuntu:22.04


# add user
ARG UNAME=tester
ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME




#install dependencies for scripts
RUN apt update

# tzdata is needed by python3, but install install it first and control the time zone so there is not a prompt that stalls the build
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York
RUN apt install -y tzdata

RUN apt install -y python3-pip ipython3 git


#install dependencies for scripts

#RUN pip3 install --break-system-packages git+https://github.com/ZZiigguurraatt/lnd-grpc-client              # how to do it cleaner than with --break-system-packages ????
RUN pip3 install git+https://github.com/ZZiigguurraatt/lnd-grpc-client
RUN pip3 install git+https://github.com/ZZiigguurraatt/python-bitcoinlib
RUN pip3 install pyyaml


#add scripts to the path statement that will be mounted by docker compose
ENV PATH="$PATH:/mini_META/scripts/"



