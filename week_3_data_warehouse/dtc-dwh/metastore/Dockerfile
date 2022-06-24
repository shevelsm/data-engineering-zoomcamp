FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

# Hive metastore installation
RUN apt-get update

RUN apt-get install -y \ 
    openjdk-11-jre-headless \
    wget

RUN apt-get clean

RUN wget "https://repo1.maven.org/maven2/org/apache/hive/hive-standalone-metastore/3.1.2/hive-standalone-metastore-3.1.2-bin.tar.gz" && \
    tar -zxvf hive-standalone-metastore-3.1.2-bin.tar.gz && \
    mv apache-hive-metastore-3.1.2-bin /usr/local/metastore

RUN wget "https://archive.apache.org/dist/hadoop/common/hadoop-3.2.1/hadoop-3.2.1.tar.gz" && \
    tar xvf hadoop-3.2.1.tar.gz && \
    mv hadoop-3.2.1 /usr/local/hadoop

RUN rm /usr/local/metastore/lib/guava-19.0.jar && \
    cp /usr/local/hadoop/share/hadoop/common/lib/guava-27.0-jre.jar \
    /usr/local/metastore/lib/ && \
    cp /usr/local/hadoop/share/hadoop/tools/lib/hadoop-aws-3.2.1.jar \
    /usr/local/metastore/lib/ && \
    cp /usr/local/hadoop/share/hadoop/tools/lib/aws-java-sdk-bundle-1.11.375.jar \
    /usr/local/metastore/lib/

RUN wget -O /usr/local/metastore/lib/mysql-connector-java-8.0.29.jar "https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.29/mysql-connector-java-8.0.29.jar"

COPY /conf /usr/local/metastore/conf
COPY entrypoint.sh /usr/local/metastore/entrypoint.sh

RUN chmod +x /usr/local/metastore/entrypoint.sh

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV HADOOP_HOME=/usr/local/hadoop
ENV METASTORE_HOME=/usr/local/metastore
ENV PATH=${METASTORE_HOME}/bin:${HADOOP_HOME}/bin:$PATH

ENTRYPOINT ["sh", "-c", "/usr/local/metastore/entrypoint.sh"]