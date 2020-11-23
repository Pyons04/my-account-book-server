import os
import sys
import json
import firebase_admin
import mysql.connector as mysql

from firebase_admin import auth, credentials
from firebase_admin.exceptions import FirebaseError

from bottle import route, run, template
from bottle import get, post, request, response

from dotenv import load_dotenv
from firebase_admin.credentials import Certificate

def getUser():
  if request.headers.get('Authorization'):
    user = auth.verify_id_token(request.headers.get('Authorization'))
    if(user):
      print('>> Current User Email: ' + user['email'])
      print('>> Current User UID  : ' + user['uid'])
      return user

@route('/user/create', method=["POST"])
def createUser():
  try: 
    user = getUser()
    mysqlCursor.execute("""
        INSERT INTO Users(uid, email) VALUES (%s, %s); 
      """, 
      (user['uid'], user['email'])
    )

    response.status = 200

  except Exception as error:
    print('>> Error :' + str(error) )
    response.status = 500
    return { 'Error' : str(error) }

@route('/transaction', method=["POST"])
def createTransacton():
  try:
    user = getUser()
    mysqlCursor.execute("""
        INSERT INTO Transactions(
          user,
          price,
          categoryKey,
          realizationDate,
          description
        ) VALUES (%s, %s, %s, %s, %s); 
      """, 
      (
        user['uid'],
        request.forms.get('price'),
        request.forms.get('categoryKey'),
        request.forms.get('realizationDate'),
        request.forms.get('description')
      )
    )
    response.status = 200
  except Exception as error:
    print('>> Error :' + str(error) )
    response.status = 500
    return { 'message' : str(error) }


@route('/category', method=["POST"])
def createCategory():
  try:
    user = getUser()
    mysqlCursor.execute("""
        INSERT INTO Categories(
          user,
          name,
          description
        ) VALUES (%s, %s, %s); 
      """, 
      (
        user['uid'],
        request.forms.get('name'),
        request.forms.get('description')
      )
    )
    response.status = 200
  except Exception as error:
    print('>> Error :' + str(error) )
    response.status = 500
    return { 'Error' : str(error) }

@route('/categories', method=["GET"])
def getCategories():
  try:
    user = getUser()
    mysqlCursor.execute("""
        SELECT 
          `key`, 
          `name`, 
          `description`, 
          DATE_FORMAT(createdDate, '%Y-%m-%d') AS createdDate
        FROM 
          Categories
        WHERE
          user = %s;          
      """, 
      (user['uid'], )
    )
    response.status = 200

    return json.dumps(mysqlCursor.fetchall(), ensure_ascii=False)

  except Exception as error:
    print('>> Error :' + str(error) )
    response.status = 500
    return { 'Error' : str(error) }


@route('/transactions', method=["GET"])
def getTransactions():
  # try:
    user = getUser()

    # NOTE: PREPAREDを利用する場合はdictionaryを利用できないため、カーソルを別途用意/For文による辞書化をする必要がある。
    designatedCursor = connection.cursor(
      prepared=True
    )

    # designatedCursor.execute("""SET @minPrice = %s;""", (2000,))
    # designatedCursor.execute("""SET @maxPrice = %s;""", (2000,))
    sql = """
      SELECT 
        `key`, 
        `price`, 
        `categoryKey`, 
        DATE_FORMAT(realizationDate, '%Y-%m-%d') AS realizationDate,
        DATE_FORMAT(createdDate,     '%Y-%m-%d') AS createdDate
      FROM 
        Transactions
      WHERE
        user = %s;
        /* AND (CASE WHEN ISNULL(@minPrice) THEN 1 ELSE price > @minPrice END) */
    """
    designatedCursor.execute(sql, (user['uid'],))
    
    keys   = designatedCursor.column_names
    values = designatedCursor.fetchall() 
    rows = []

    for value in values:
      rows.append(dict(zip(keys, value)))

    designatedCursor.close()
    response.status = 200   
    return json.dumps(rows, ensure_ascii=False)

  # except Exception as error:
  #   print('>> Error :' + str(error) )
  #   response.status = 500
  #   return { 'Error' : str(error) }

load_dotenv(verbose=True)
firebaseCredential = {
  "type": "service_account",
  "project_id":     os.getenv("project_id"),
  "private_key_id": os.getenv("private_key_id"),
  "private_key":    os.getenv("private_key"),
  "client_email":   os.getenv("client_email"),
  "client_id":      os.getenv("client_id"),
  "token_uri":      "https://oauth2.googleapis.com/token",
  "client_x509_cert_url": os.getenv("client_x509_cert_url")
 }

default_app = firebase_admin.initialize_app(credential= Certificate(firebaseCredential))
config = {
  'host' :     os.getenv("DB_HOSTNAME"),
  'port':      os.getenv("DB_PORT"),
  'user':      os.getenv("USER"),
  'password' : os.getenv("DB_PASSWORD"),
  'database' : 'MyAccountBook'
}
connection = mysql.connect(**config)
connection.ping(reconnect=True)
connection.autocommit = True

mysqlCursor = connection.cursor(
  buffered=True,
  dictionary=True, 
)
run(host='0.0.0.0', port=os.getenv("PORT"), debug=True)
