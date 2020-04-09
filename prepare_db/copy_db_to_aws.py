from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client1 = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db1 = client1.publicfund                    # 'publicfund'라는 이름의 db를 만듭니다.

client2 = MongoClient('mongodb://spartahoya:123456@15.164.222.219', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db2 = client2.publicfund                    # 'publicfund'라는 이름의 db를 만듭니다.

infos = list(db1.funds.find({},{'_id':0})) # [{1},{2},{3}..]
db2.funds.insert_many(infos)  # robot3T 안에 있는 publicfund shell 안에 collection 안에 있는 document 이름이 funds


# aws 에다가 올려주기 (서버에서도 로컬처럼 보여주고 돌리기 위해서)