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
('고씨네 돈까스 카레','F001'),
('고씨네 스페셜 카레','F002'),
('고씨네 프리미엄 카레','F003'),
('돈까스 카레 우동','F004'),
('버섯 카레 우동','F005'),
('버섯 카레','F006'),

('스테이크삼겹정식','F007'),
('스테이크정식(소)','F008'),
('삼겹테이크정식(소)','F009'),
('안창불고기스테이크정식','F010'),
('목살스테이크볶음밥','F011'),
('모듬스테이크정식','F012'),

('김치돈까스나베','F013'),
('할라피뇨연어덮밥','F014'),
('수제돈까스','F015'),
('해물야끼우동','F016'),
('달인냉우동','F017'),
('마약냉우동','F018'),

('아주세트','F019'),
('치즈세트','F020'),
('치즈더블세트','F021'),
('솥뚜껑 해물파전','F022'),
('철판 모듬 스페셜','F023'),
('철판 제육 볶음','F024'),

('닭갈비철판볶음밥','F025'),
('매운철판볶음밥','F026'),
('모듬철판볶음밥','F027'),
('유가네닭갈비','F028'),
('미소허니퐁닭','F029'),
('해물철판볶음밥','F030'),

('그릴 목살 스테이크','F031'),
('살치살 소고기 스테이크','F032'),
('핫치킨 꿀치즈 퀘사디아','F033'),
('페퍼로니 토마토 퀘사디아','F034'),
('소고기 감자 스튜','F035'),
('모든치즈크래커','F036'),

('돈코츠라멘','F037'),
('소유라멘','F038'),
('미소라멘','F039'),
('규동','F040'),
('부타동','F041'),
('차슈동','F042'),

('치킨라이스','F043'),
('치킨감자','F044'),
('소고기라이스','F045'),
('소세지감자','F046'),
('새우감자','F047'),
('핫도그','F048'),

('해물뚝배기','F049'),
('제육두루치기','F050'),
('참치김치찌개','F051'),
('카레덮밥','F052'),
('돈까스덮밥','F053'),
('곱창순두부찌개','F054'),

('봉구스밥버거','F055'),
('햄치즈밥버거','F056'),
('치즈제육밥버거','F057'),
('청양불고기밥버거','F058'),
('소불고기밥버거','F059'),
('통살돈까스마요밥버거','F060'),

('소고기 쌀국수','F061'),
('닭 쌀국수','F062'),
('사이공 볶음밥','F063'),
('사이공 볶음면','F064'),
('새우볼','F065'),
('사이공 딤섬','F066'),

('후라이드','F067'),
('양념','F068'),
('간장','F069'),
('스위트갈릭','F070'),
('스위트버터','F071'),
('반반치킨','F072'),

('짜장면','F073'),
('짱뽕','F074'),
('삼선짬뽕','F075'),
('찹쌀탕수육','F076'),
('양꼬치','F077'),
('군만두','F078'),

]

DATA_TABLES['FOOD_TYPE'] = [ 
('한식',        'T001'),
('일식',        'T002'),
('중식',        'T003'),
('양식',        'T004'),
('술집',        'T005'),
('기타',        'T006')
]

DATA_TABLES['COOKED_BY'] = [ 
('F001',        'R001'),
('F002',        'R001'),
('F003',        'R001'),
('F004',        'R001'),
('F005',        'R001'),
('F006',        'R001'),

('F007',        'R002'),
('F008',        'R002'),
('F009',        'R002'),
('F010',        'R002'),
('F011',        'R002'),
('F012',        'R002'),

('F013',        'R003'),
('F014',        'R003'),
('F015',        'R003'),
('F016',        'R003'),
('F017',        'R003'),
('F018',        'R003'),

('F019',        'R004'),
('F020',        'R004'),
('F021',        'R004'),
('F022',        'R004'),
('F023',        'R004'),
('F024',        'R004'),

('F025',        'R005'),
('F026',        'R005'),
('F027',        'R005'),
('F028',        'R005'),
('F029',        'R005'),
('F030',        'R005'),

('F031',        'R006'),
('F032',        'R006'),
('F033',        'R006'),
('F034',        'R006'),
('F035',        'R006'),
('F036',        'R006'),

('F037',        'R007'),
('F038',        'R007'),
('F039',        'R007'),
('F040',        'R007'),
('F041',        'R007'),
('F042',        'R007'),

('F043',        'R008'),
('F044',        'R008'),
('F045',        'R008'),
('F046',        'R008'),
('F047',        'R008'),
('F048',        'R008'),

('F049',        'R009'),
('F050',        'R009'),
('F051',        'R009'),
('F052',        'R009'),
('F053',        'R009'),
('F054',        'R009'),

('F055',        'R010'),
('F056',        'R010'),
('F057',        'R010'),
('F058',        'R010'),
('F059',        'R010'),
('F060',        'R010'),

('F061',        'R011'),
('F062',        'R011'),
('F063',        'R011'),
('F064',        'R011'),
('F065',        'R011'),
('F066',        'R011'),

('F067',        'R012'),
('F068',        'R012'),
('F069',        'R012'),
('F070',        'R012'),
('F071',        'R012'),
('F072',        'R012'),

('F073',        'R013'),
('F074',        'R013'),
('F075',        'R013'),
('F076',        'R013'),
('F077',        'R013'),
('F078',        'R013'),
]

#한식:T001 일식:T002  중식:T003  양식:T004  술집:T005  기타:T006
DATA_TABLES['RESTAURANT'] = [ #20ea
('고씨네',       'R001','T002','https://m.store.naver.com/restaurants/detail?id=37269016&query=%EA%B3%A0%EC%94%A8%EB%84%A4%20%EC%95%84%EC%A3%BC%EB%8C%80%EC%A0%90&entry=plt&back=false','6000~9500'),
('모모스테이크',  'R002','T004','https://m.store.naver.com/restaurants/detail?id=36412392&query=%EB%AA%A8%EB%AA%A8%EC%8A%A4%ED%85%8C%EC%9D%B4%ED%81%AC%20%EC%95%84%EC%A3%BC%EB%8C%80%EC%A0%90&entry=plt','8500~16000'),
('천애부',       'R003','T002','https://m.store.naver.com/restaurants/detail?id=33875226&query=%EC%B2%9C%EC%95%A0%EB%B6%80%EB%8B%AC%EC%9D%B8%EC%9A%B0%EB%8F%99&entry=plt','2000~9500'),
('일미닭갈비',    'R004','T001','https://m.store.naver.com/restaurants/detail?id=38485469&query=%EC%9D%BC%EB%AF%B8%EB%8B%AD%EA%B0%88%EB%B9%84%ED%8C%8C%EC%A0%84&entry=plt','6900~14000'),
('유가네닭갈비',  'R005','T001','https://m.store.naver.com/restaurants/detail?id=21102801&query=%EC%95%84%EC%A3%BC%EB%8C%80%20%EC%9C%A0%EA%B0%80%EB%84%A4%EB%8B%AD%EA%B0%88%EB%B9%84','4500~28000'),
('Mr.Chef Pocha','R006','T004','https://m.store.naver.com/restaurants/detail?id=21278958&query=%EB%AF%B8%EC%8A%A4%ED%84%B0%EC%89%90%ED%94%84%ED%8F%AC%EC%B0%A8&entry=plt','9500~50000'),
('멘야고이치',    'R007','T002','https://m.store.naver.com/restaurants/detail?id=20322446','6500~7500'),
('밀플랜비',      'R008','T006','https://m.store.naver.com/restaurants/detail?id=38009073&query=%EB%B0%80%ED%94%8C%EB%9E%9C%EB%B9%84%20%EC%95%84%EC%A3%BC%EB%8C%80%EC%A0%90&entry=plt','3000~6000'),
('Mr.chef',      'R009','T001','https://m.store.naver.com/restaurants/detail?id=30811729&query=%EB%AF%B8%EC%8A%A4%ED%84%B0%EC%89%90%ED%94%84&entry=plt','5500~8000')
('봉구스밥버거',    'R010','T001','https://m.store.naver.com/restaurants/detail?id=31077787','1800~3500'),
('미스사이공',    'R011','T006','https://m.store.naver.com/restaurants/detail?id=38762477&query=%EC%95%84%EC%A3%BC%EB%8C%80%20%EB%AF%B8%EC%8A%A4%EC%82%AC%EC%9D%B4%EA%B3%B5','3900~4900'),
('도담도담치킨',    'R012','T006','https://m.store.naver.com/restaurants/detail?id=36655478&entry=plt','15000~16000'),
('뽕스토리',    'R013','T003','https://m.store.naver.com/restaurants/detail?id=342201261&query=%EB%AF%B8%EA%B0%81%EC%96%91%EA%BC%AC%EC%B9%98&%EB%BD%95%EC%8A%A4%ED%86%A0%EB%A6%AC&entry=plt','4500~35000'),
#('봉구스밥버거',    'R014','T001','https','6500~7500'),
#('봉구스밥버거',    'R015','T001','https','6500~7500'),
#('봉구스밥버거',    'R016','T001','https','6500~7500'),
#('봉구스밥버거',    'R017','T001','https','6500~7500'),
#('봉구스밥버거',    'R018','T001','https','6500~7500'),
#('봉구스밥버거',    'R019','T001','https','6500~7500'),
#('봉구스밥버거',    'R020','T001','https','6500~7500'),
#('봉구스밥버거',    'R021','T001','https','6500~7500'),
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