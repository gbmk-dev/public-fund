from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
# client = MongoClient('mongodb://spartahoya:123456@15.164.222.219', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
client = MongoClient('mongodb://localhost', 27017)
db = client.publicfund                    # 'publicfund'라는 이름의 db를 만듭니다.



## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('public_fund.html')


#검색창에 클라이언트가 입력을 하면, 그때 자동완성 List 띄어주는 API
@app.route('/fund', methods=['GET'])
def f_list_active_name():
    result = list(db.funds.find({'Status': "Active"}, {'_id': 0}))  # 필터링 리스트
    return jsonify(result)



#검색한 펀드의 운용역 이름이 포함된 List를 불러오는 API
@app.route('/fund', methods=['POST'])
def fm_past():
    fund_name_receive = request.form['fund_name_give']
    manager_name = fund_name_receive.split(':')[0].strip()
    fund_name = fund_name_receive.split(':')[1].strip()
    print(fund_name_receive, fund_name, manager_name)
    target_fund_info = db.funds.find_one({'Status': "Active", 'fund_name':fund_name, 'manager_name': manager_name}, {'_id': 0}) #id값은 가져오지 않겠다
    print(target_fund_info)
    funds_info = list(db.funds.find({'Status': "Past",'manager_name':target_fund_info['manager_name']}, {'_id': 0}))  # 현재 운영중인 펀드매니저 이름이랑 매칭 되는 과거 내역들을 가져와라
    print(funds_info)
    return jsonify(funds_info)

#Port를 설정하는 Coding
if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)


#책임 운용사, 투자일, 회수일, 수익률 front ajax 들어감

