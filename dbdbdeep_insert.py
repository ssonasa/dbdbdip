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
  cnx = mysql.connector.connect(host= 'dbdbdeep.co7zvonejcs7.ap-northeast-2.rds.amazonaws.com',
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
('카레','F145'),
('고씨네 돈까스 카레','F001'),
('고씨네 스페셜 카레','F002'),
('고씨네 프리미엄 카레','F003'),
('돈까스 카레 우동','F004'),
('버섯 카레 우동','F005'),
('버섯 카레','F006'),

('스테이크','F146'),
('스테이크삼겹정식','F007'),
('스테이크정식(소)','F008'),
('삼겹테이크정식(소)','F009'),
('안창불고기스테이크정식','F010'),
('목살스테이크볶음밥','F011'),
('모듬스테이크정식','F012'),

('우동','F147'),
('김치돈까스나베','F013'),
('할라피뇨연어덮밥','F014'),
('수제돈까스','F015'),
('해물야끼우동','F016'),
('달인냉우동','F017'),
('마약냉우동','F018'),

('닭갈비','F148'),
('아주세트','F019'),
('치즈세트','F020'),
('치즈더블세트','F021'),
('솥뚜껑 해물파전','F022'),
('철판 모듬 스페셜','F023'),
('철판 제육 볶음','F024'),

('닭갈비','F148'),
('닭갈비철판볶음밥','F025'),
('매운철판볶음밥','F026'),
('모듬철판볶음밥','F027'),
('유가네닭갈비','F028'),
('미소허니퐁닭','F029'),
('해물철판볶음밥','F030'),

('스테이크','F146'),
('그릴 목살 스테이크','F031'),
('살치살 소고기 스테이크','F032'),
('핫치킨 꿀치즈 퀘사디아','F033'),
('페퍼로니 토마토 퀘사디아','F034'),
('소고기 감자 스튜','F035'),
('모든치즈크래커','F036'),

('라멘','F149'),
('돈코츠라멘','F037'),
('소유라멘','F038'),
('미소라멘','F039'),
('규동','F040'),
('부타동','F041'),
('차슈동','F042'),

('부리또','F150'),
('치킨라이스','F043'),
('치킨감자','F044'),
('소고기라이스','F045'),
('소세지감자','F046'),
('새우감자','F047'),
('핫도그','F048'),

('제육볶음','F151'),
('해물뚝배기','F049'),
('제육두루치기','F050'),
('참치김치찌개','F051'),
('카레덮밥','F052'),
('돈까스덮밥','F053'),
('곱창순두부찌개','F054'),

('밥버거','F152'),
('봉구스밥버거','F055'),
('햄치즈밥버거','F056'),
('치즈제육밥버거','F057'),
('청양불고기밥버거','F058'),
('소불고기밥버거','F059'),
('통살돈까스마요밥버거','F060'),

('쌀국수','F153'),
('소고기 쌀국수','F061'),
('닭 쌀국수','F062'),
('사이공 볶음밥','F063'),
('사이공 볶음면','F064'),
('새우볼','F065'),
('사이공 딤섬','F066'),

('치킨','F154'),
('크리스피','F067'),
('양념치킨','F068'),
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

('알밥','F155'),
('순한알밥','F079'),
('매콤알밥','F080'),
('매콤치즈알밥','F081'),
('카레알밥','F082'),
('갈릭알밥','F083'),
('갈립치즈알밥','F084'),

('삼겹살','F156'),
('벌집삼겹살','F085'),
('돼지왕구이','F086'),
('갈비탕','F087'),
('김치말이국수','F088'),
('냉면','F089'),
('항정살','F090'),

('찜닭','F157'),
('고추장찜닭','F091'),
('안동찜닭','F092'),
('순살안동장찜닭','F093'),
('순살고추장찜닭','F094'),
('치즈순살찜닭중','F095'),
('치즈순살찜닭대','F096'),


('부대찌개','F097'),
('김치찌개','F098'),
('주먹밥','F099'),
('계란말이','F100'),
('라면','F101'),
('만두','F102'),

('부대찌개','F097'),
#('부대찌개','F103'), F098
('육계장','F104'),
#('갈비탕','F105'), F087
('제육볶음','F106'),
('순두부찌개','F107'),
#('김치찌개','F108'), F097

('곱창','F158'),
('양구이','F109'),
('대창구이','F110'),
('곱창구이','F111'),
('막창구이','F112'),
('천엽','F113'),
('곱창전골','F114'),

('치킨','F154'),
('전설의치킨','F115'),
('칠리새우순살','F116'),
#('양념치킨','F117'), F068
#('크리스피','F118'), F067
('순살파닭','F119'),
('치킨떡볶이','F120'),

('소고기','F159'),
('소한마리(생고기)','F121'),
('소한마리(주물럭)','F122'),
#('김치말이국수','F123'), F088
('소고기국수','F124'),
('비빔국수','F125'),
('우거지국','F126'),

('볶음밥','F160'),
('돌판삼겹살','F127'),
('돌판닭갈비','F128'),
('돌판제육볶음','F129'),
('돌판날치알밥','F130'),
('돌판힐링볶음밥','F131'),
('돌판소불고기','F132'),

('덮밥','F161'),
('와규덮밥','F133'),
('생연어덮밥','F134'),
#('차슈덮밥','F135'),F042
#('부타동덮밥','F136'), F041
('가츠동덮밥','F137'),
('에비동덮밥','F138'),

('족발','F162'),
('참족발앞다리','F139'),
('불족발앞다리','F140'),
('석쇠구이족발앞다리','F141'),
('반반족발앞다리','F142'),
#('주먹밥','F143'), F099
('메밀전병','F144')

#('돌판힐링볶음밥','F145'),
#('돌판힐링볶음밥','F146'),
#('돌판힐링볶음밥','F147'),
#('돌판힐링볶음밥','F148'),
#('돌판힐링볶음밥','F149'),
#('돌판힐링볶음밥','F150')

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

('F079',        'R014'),
('F080',        'R014'),
('F081',        'R014'),
('F082',        'R014'),
('F083',        'R014'),
('F084',        'R014'),

('F085',        'R015'),
('F086',        'R015'),
('F087',        'R015'),
('F088',        'R015'),
('F089',        'R015'),
('F090',        'R015'),

('F091',        'R016'),
('F092',        'R016'),
('F093',        'R016'),
('F094',        'R016'),
('F095',        'R016'),
('F096',        'R016'),

('F097',        'R017'),
('F098',        'R017'),
('F099',        'R017'),
('F100',        'R017'),
('F101',        'R017'),
('F102',        'R017'),

('F098',        'R018'),
('F104',        'R018'),
('F087',        'R018'),
('F106',        'R018'),
('F107',        'R018'),
('F097',        'R018'),

('F109',        'R019'),
('F110',        'R019'),
('F111',        'R019'),
('F112',        'R019'),
('F113',        'R019'),
('F114',        'R019'),

('F115',        'R020'),
('F116',        'R020'),
('F068',        'R020'),
('F067',        'R020'),
('F119',        'R020'),
('F120',        'R020'),

('F121',        'R021'),
('F122',        'R021'),
('F088',        'R021'),
('F124',        'R021'),
('F125',        'R021'),
('F126',        'R021'),

('F127',        'R022'),
('F128',        'R022'),
('F129',        'R022'),
('F130',        'R022'),
('F131',        'R022'),
('F132',        'R022'),

('F133',        'R023'),
('F134',        'R023'),
('F042',        'R023'),
('F041',        'R023'),
('F137',        'R023'),
('F138',        'R023'),

('F139',        'R024'),
('F140',        'R024'),
('F141',        'R024'),
('F142',        'R024'),
('F099',        'R024'),
('F144',        'R024'),

('F145',        'R001'),
('F146',        'R002'),
('F146',        'R006'),
('F147',        'R003'),

('F148',        'R004'),
('F148',        'R005'),

('F149',        'R007'),
('F150',        'R008'),
('F151',        'R009'),

('F152',        'R010'),
('F153',        'R011'),
('F154',        'R012'),
('F154',        'R020'),

('F155',        'R014'),
('F156',        'R015'),
('F157',        'R016'),
('F158',        'R019'),
('F159',        'R021'),
('F160',        'R022'),
('F161',        'R023'),
('F162',        'R024')

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
('봉구스밥버거',  'R010','T001','https://m.store.naver.com/restaurants/detail?id=31077787','1800~3500'),
('미스사이공',    'R011','T006','https://m.store.naver.com/restaurants/detail?id=38762477&query=%EC%95%84%EC%A3%BC%EB%8C%80%20%EB%AF%B8%EC%8A%A4%EC%82%AC%EC%9D%B4%EA%B3%B5','3900~4900'),
('도담도담치킨',  'R012','T006','https://m.store.naver.com/restaurants/detail?id=36655478&entry=plt','15000~16000'),
('뽕스토리',      'R013','T003','https://m.store.naver.com/restaurants/detail?id=342201261&query=%EB%AF%B8%EA%B0%81%EC%96%91%EA%BC%AC%EC%B9%98&%EB%BD%95%EC%8A%A4%ED%86%A0%EB%A6%AC&entry=plt','4500~35000'),
('알촌',          'R014','T001','https://m.store.naver.com/restaurants/detail?id=32848717&query=%EC%95%8C%EC%B4%8C%20%EC%95%84%EC%A3%BC%EB%8C%80%EC%A0%90&entry=plt','3500~4800'),
('벌집삼겹살',     'R015','T001','https://m.store.naver.com/restaurants/detail?id=19438153&query=%EB%B2%8C%EC%A7%91%EC%82%BC%EA%B2%B9%EC%82%B4%20%EC%95%84%EC%A3%BC%EB%8C%80%EC%A0%90&entry=plt','3500~11900'),
('내가찜한닭',     'R016','T001','https://m.store.naver.com/restaurants/detail?id=33471257&query=%EB%82%B4%EA%B0%80%EC%B0%9C%ED%95%9C%EB%8B%AD%20%EC%95%84%EC%A3%BC%EB%8C%80%EC%A0%90&entry=plt','17000~39000'),
('맛구단',         'R017','T001','https://m.search.naver.com/search.naver?where=m&sm=mtb_jum&query=%EC%95%84%EC%A3%BC%EB%8C%80+%EB%A7%9B%EA%B5%AC%EB%8B%A8','2000~22000'),
('찌개백반',       'R018','T001','https://m.store.naver.com/restaurants/detail?id=18226632','5000~8000'),
('서울곱창',       'R019','T001','https://m.store.naver.com/restaurants/detail?id=18227763&query=%EC%84%9C%EC%9A%B8%EA%B3%B1%EC%B0%BD&entry=plt','17000~50000'),
('전설의치킨',     'R020','T001','https://m.store.naver.com/restaurants/detail?id=37811564&query=%EC%A0%84%EC%84%A4%EC%9D%98%EC%B9%98%ED%82%A8%20%EC%95%84%EC%A3%BC%EB%8C%80%EC%A0%90&entry=plt','11000~1400'),
('반값소',         'R021','T001','https://m.store.naver.com/restaurants/detail?id=37592424&query=%EB%B0%98%EA%B0%92%EC%86%8C&entry=plt','3000~39000'),
('푸드테라피',    'R022','T001','https://m.store.naver.com/restaurants/detail?id=33133453&query=%ED%91%B8%EB%93%9C%ED%85%8C%EB%9D%BC%ED%94%BC&entry=plt','5000~7000')
('만고쿠',         'R023','T002','https://m.store.naver.com/restaurants/detail?id=37342139&query=%EB%A7%8C%EA%B3%A0%EC%BF%A0&entry=plt','4000~8000'),
('우만동족발집',    'R024','T001','https://m.store.naver.com/restaurants/detail?id=36424455','3000~36000')
#('푸드테라피',    'R022','T001','https','5000~7000'),
#('푸드테라피',    'R022','T001','https','5000~7000'),
#('푸드테라피',    'R022','T001','https','5000~7000'),
#('푸드테라피',    'R022','T001','https','5000~7000'),
#('푸드테라피',    'R022','T001','https','5000~7000'),
#('푸드테라피',    'R022','T001','https','5000~7000'),

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