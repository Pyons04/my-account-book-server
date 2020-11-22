import os
import mysql.connector as mysql
from dotenv import load_dotenv

load_dotenv(verbose=True)

config = {
  'host' :     os.getenv("DB_HOSTNAME"),
  'port':      os.getenv("DB_PORT"),
  'user':      os.getenv("USER"),
  'password' : os.getenv("DB_PASSWORD")
}

connection = mysql.connect(**config)
mysqlCursor = connection.cursor()
mysqlCursor.execute(" CREATE DATABASE IF NOT EXISTS MyAccountBook ")

mysqlCursor.close()
connection.close()

config['database'] = 'MyAccountBook'
connection  = mysql.connect(**config)

mysqlCursol = connection.cursor()
mysqlCursol.execute(""" 
   CREATE TABLE IF NOT EXISTS Users (
    `uid`   varchar(50) not null PRIMARY KEY,
    `email` varchar(50) not null,
    `createdDate` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )"""
)

mysqlCursol.execute(""" 
   CREATE TABLE IF NOT EXISTS Categories (
    `key`   MEDIUMINT   not null PRIMARY KEY AUTO_INCREMENT,
    `user`  varchar(50) not null,
    `name`  varchar(50) not null,
    `description` varchar(300),
    `createdDate` timestamp not null DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(user) REFERENCES Users(uid)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    )"""
)

mysqlCursol.execute(""" 
   CREATE TABLE IF NOT EXISTS Transactions (
    `key`   MEDIUMINT not null PRIMARY KEY AUTO_INCREMENT,
    `user`      varchar(50) not null,
    `price`       MEDIUMINT not null,
    `categoryKey` MEDIUMINT not null,
    `realizationDate` DATETIME not null,
    `createdDate` timestamp not null DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `description` varchar(300),
    FOREIGN KEY(user) REFERENCES Users(uid)
      ON UPDATE CASCADE
      ON DELETE RESTRICT,
    FOREIGN KEY(categoryKey) REFERENCES Categories(`key`)
      ON UPDATE CASCADE
      ON DELETE RESTRICT
   )"""
)

mysqlCursol.close()
connection.close()