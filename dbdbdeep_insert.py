#-*-coding: utf-8 -*-


from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
import os
from mysql.connector import errorcode

DB_NAME = 'dbdbdeep'
print("DB loading...\n\n")
#login(connect to mysql)---------------------------------------------------------------------------------
try:
  cnx = mysql.connector.connect(host= 'choosethis.cemhkd80ccxj.us-east-2.rds.amazonaws.com',
                                user='blcocas',
                                password = '201221027',
                                charset='utf8mb4')
  cursor = cnx.cursor()
  print("success to connect")

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

#create database-----------------------------------------------------------------------------------------
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        print("success to creat DB")
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cnx.database = DB_NAME  
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

#Relation-----------------------------------------------------------------------------------------------

TABLES = {}

TABLES['FOOD'] = (
"CREATE TABLE  `FOOD`(" 
"`Food_Name`        varchar(15)     NOT NULL,"
"`Food_Num`         char(8)         NOT NULL,"
"PRIMARY KEY (`Food_Num`)"
") ENGINE=InnoDB")


TABLES['FOOD_TYPE'] = (
"CREATE TABLE  `FOOD_TYPE` ("
"`Type_Name`       varchar(15)       NOT NULL,"
"`Type_Num`        char(8)           NOT NULL,"
"PRIMARY KEY (`Type_Num`)"
")ENGINE=InnoDB")

TABLES['COOKED_BY'] = (
"CREATE TABLE  `COOKED_BY` ("   
"`F_Num`        char(8)     NOT NULL,"
"`R_Num`        char(8)     NOT NULL,"
"PRIMARY KEY(`F_Num`, `R_Num`),"
"FOREIGN KEY (`F_Num`) REFERENCES `FOOD`(`Food_Num`),"
"FOREIGN KEY (`R_Num`) REFERENCES `RESTAURANT`(`Rest_Num`)"
")ENGINE=InnoDB")

    
TABLES['RESTAURANT'] = (
"CREATE TABLE  RESTAURANT ( "
"`Rest_Name`       varchar(15)     NOT NULL,"
"`Rest_Num`        char(8)     NOT NULL,"
"`T_Num`           char(8)     NOT NULL,"
"`Map`            varchar(100)     ,"
"`Average_Cost`    varchar(15)         ,"
"PRIMARY KEY (`Rest_Num`),"
"FOREIGN KEY (`T_Num`) REFERENCES FOOD_TYPE(`Type_Num`)"
")ENGINE=InnoDB")



 #foreign key constraints unlock argument-----------------------------------------------------------------               

disable_foreign = ''' 
    SET FOREIGN_KEY_CHECKS = 0;
'''
enable_foreign = ''' 
    SET FOREIGN_KEY_CHECKS = 1;
'''

#create tables------------------------------------------------------------------------------------------
cursor.execute(disable_foreign) #foreign key constraint no check

for name, ddl in TABLES.iteritems():
    try:
        print("Creating table {}: ".format(name), end='')
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")
#insert data form---------------------------------------------------------------------------------------
INSERT_TABLES = {}
INSERT_TABLES['FOOD'] = ("INSERT INTO FOOD "
            "(Food_Name, Food_Num)"
            "VALUES (%s, %s)")

INSERT_TABLES['FOOD_TYPE'] = ("INSERT INTO FOOD_TYPE "
            "(Type_Name,Type_Num)"
            "VALUES (%s, %s)")

INSERT_TABLES['COOKED_BY'] = ("INSERT INTO COOKED_BY "
            "(F_Num,R_Num)"
            "VALUES (%s, %s)")

INSERT_TABLES['RESTAURANT'] = ("INSERT INTO RESTAURANT "
            "(Rest_Name,Rest_Num,T_Num,Map,Average_Cost)"
            "VALUES (%s, %s, %s, %s, %s)")

#tuples-------------------------------------------------------------------------------------------------
DATA_TABLES = {}
DATA_TABLES['FOOD'] = [ #40ea
('삼겹살','F001'),
('라면','F002'),
('찜닭','F003'),
('부대찌개','F004'),
('쌀국수','F005'),
('짜장면','F006'),
('짬뽕','F007'),
('햄버거','F008')
]

DATA_TABLES['FOOD_TYPE'] = [ #20ea
('한식',        'T001'),
('일식',        'T002'),
('중식',        'T003'),
('양식',        'T004'),
('술집',        'T005'),
('기타',        'T006')
]

DATA_TABLES['COOKED_BY'] = [ #20ea
('F001',        'R001'),
('F001',        'R003'),
('F002',        'R002'),
('F003',        'R004'),
('F004',        'R007'),
('F005',        'R009'),
('F006',        'R008'),
('F007',        'R008'),
('F008',        'R006')
]

DATA_TABLES['RESTAURANT'] = [ #20ea
('벌집삼겹살',   'R001','T001','https://m.search.naver.com/search.naver?query=%EC%95%84%EC%A3%BC%EB%8C%80+%EB%B2%8C%EC%A7%91%EC%82%BC%EA%B2%B9%EC%82%B4&where=m&sm=mtp_hty','10000~15000'),
('멘야고이쿠치',  'R002','T002','https://m.store.naver.com/restaurants/detail?id=20322446','5000~10000'),
('생고기대학교',  'R003','T001','',''),
('꽃찬찜닭',    'R004','T001','',''),
('모모스테이크',  'R005','T004','',''),
('맥도날드',     'R006','T004','',''),
('할머니부대찌개',  'R007','T001','',''),
('짜장맛좀보실래요',  'R008','T003','',''),
('미스사이공',       'R009','T006','','')

]
#data insert----------------------------------------------------------------------------------------------
for name, insert_form in INSERT_TABLES.iteritems():
    try:
        print("Inserting tuples to TABLE({})\n".format(name), end='')
        for data in DATA_TABLES[name]: 
            try:
                cursor.execute(insert_form,data)
            except mysql.connector.Error as err:
                print("{}({})".format(err.msg,name))
    except mysql.connector.Error as err:
        if(err):
            print(err.msg)
        else:
            print("OK")

cursor.execute(enable_foreign) #foreign key constraint check
cnx.commit()


#query----------------------------------------------------------------------------------------------------



#print form----------------------------------------------------------------------------------------------

   
#operation-----------------------------------------------------------------------------------------------

    
#main-----------------------------------------------------------------------------------------------------


cursor.close()
cnx.close()