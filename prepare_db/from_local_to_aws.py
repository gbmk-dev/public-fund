from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client_local = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db_local = client_local.publicfund                    # 'publicfund'라는 이름의 db를 만듭니다.

client_aws = MongoClient('mongodb://spartahoya:123456@15.164.222.219', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db_aws = client_aws.publicfund # 'publicfund'라는 이름의 db를 만듭니다.

coll_names = [collection for collection in db_local.list_collection_names()]
for col_name in coll_names:
    print("aws ", col_name, " 삭제")
    db_aws[col_name].drop()

    docs = list(db_local[col_name].find({}, {'_id': False}))
    db_aws[col_name].insert_many(docs)
    print("local -> aws: collection", col_name)