FROM python:latest
COPY . .
RUN apt-get update -yqq \
    && apt-get install -y --no-install-recommends openssl \
    && sed -i 's,^\(MinProtocol[ ]*=\).*,\1'TLSv1.0',g' /etc/ssl/openssl.cnf \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get install -y git
RUN pip install firebase_admin mysqlclient mysql-connector-python python-dotenv bottle
RUN python app/initializeDb.py
CMD ["python", "app/main.py"]