
FROM ubuntu
ADD . .
WORKDIR .
RUN apt-get update
RUN apt-get -s upgrade
RUN apt-get install sudo
RUN sudo apt install sqlite3 -y
RUN sudo apt-get install curl gnupg apt-transport-https -y
RUN curl -1sLf "https://keys.openpgp.org/vks/v1/by-fingerprint/0A9AF2115F4687BD29803A206B73A36E6026DFCA" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/com.rabbitmq.team.gpg > /dev/null
RUN curl -1sLf "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xf77f1eda57ebb1cc" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/net.launchpad.ppa.rabbitmq.erlang.gpg > /dev/null
RUN curl -1sLf "https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/io.packagecloud.rabbitmq.gpg > /dev/null
RUN sudo apt-get update -y
RUN sudo apt-get install -y erlang-base erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key erlang-runtime-tools erlang-snmp erlang-ssl erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl
RUN sudo apt-get install rabbitmq-server -y --fix-missing
RUN sudo rabbitmq-plugins enable rabbitmq_management
RUN service rabbitmq-server start
RUN apt-get install -y python3-pip
RUN pip install -r requirements.txt
CMD ["python3", "runserv.py"]
