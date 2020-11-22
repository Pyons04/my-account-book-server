FROM python:latest
RUN apt-get update -yqq \
    && apt-get install -y --no-install-recommends openssl \
    && sed -i 's,^\(MinProtocol[ ]*=\).*,\1'TLSv1.0',g' /etc/ssl/openssl.cnf \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get install -y git
RUN git clone https://github.com/Pyons04/my-account-book-server.git
COPY app/.env /my-account-book-server/app/.env

RUN pip install firebase_admin mysqlclient mysql-connector-python python-dotenv bottle
RUN python /my-account-book-server/app/initializeDb.py
CMD ["python", "my-account-book-server/app/main.py"]