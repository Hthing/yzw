FROM alpine
  
ENV LANG=C.UTF-8


RUN echo "http://mirrors.aliyun.com/alpine/latest-stable/main/" > /etc/apk/repositories && \
    echo "http://mirrors.aliyun.com/alpine/latest-stable/community/" >> /etc/apk/repositories
  
  

RUN apk update && \
    apk add --no-cache openssh-server tzdata && \
    sed -i "s/#PermitRootLogin.*/PermitRootLogin yes/g" /etc/ssh/sshd_config && \
    ssh-keygen -t rsa -P "" -f /etc/ssh/ssh_host_rsa_key && \
    ssh-keygen -t ecdsa -P "" -f /etc/ssh/ssh_host_ecdsa_key && \
    ssh-keygen -t ed25519 -P "" -f /etc/ssh/ssh_host_ed25519_key && \
    echo "root:h056zHJLg85oW5xh7VtSa" | chpasswd
 
 

RUN apk add --no-cache python3 python3-dev gcc openssl-dev openssl libressl libc-dev linux-headers libffi-dev libxml2-dev libxml2 libxslt-dev openssh-client openssh-sftp-server
RUN pip3 install --default-timeout=100 --no-cache-dir --upgrade pip setuptools pymysql Scrapy xlwt

RUN echo "/usr/sbin/sshd -D" >> /etc/start.sh && \
    chmod +x /etc/start.sh
WORKDIR /home
RUN wget https://github.com/Hthing/yzw/archive/master.zip && unzip master.zip
WORKDIR ./yzw-master
    



EXPOSE 22
  
# 执行ssh启动命令
CMD ["/bin/sh","/etc/start.sh"]