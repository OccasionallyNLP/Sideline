from flask import Flask, render_template, request
import pymongo

def find_things(leisure, input:dict):
    # 시설종목명 or 시도명
    시설종목명 = input['시설종목명'].upper()
    시도명 = input['시도명']
    if 시설종목명 and 시도명:
        return leisure.find({'시설종목명':{'$in':[시설종목명]}, '시도명':{'$in':[시도명]}})
    if 시설종목명 and not 시도명:
        return leisure.find({'시설종목명':{'$in':[시설종목명]}})
    if not 시설종목명 and 시도명:
        return leisure.find({'시도명':{'$in':[시도명]}})    

app = Flask(__name__)
 
@app.route('/')
def inputTest(facility_type=None, location=None):
    return render_template('main.html', facility_type=facility_type, location=location)

@app.route('/find',methods=['POST'])
def find_corps(facility_type=None, location=None):
    if request.method == 'POST':
        facility_type = request.form['facility_type']
        location = request.form['location']
    else:
        facility_type = None
        location = None
    
    connection = pymongo.MongoClient() # basic port : 27017
    # database instance화
    database = connection.database # database에 database가 없어도 자동 생성함.
    # db 이름 확인
    leisure = database.corporations
    response = find_things(leisure, dict(시설종목명=facility_type,시도명=location))
    return render_template('main_2.html', data=response)
    
if __name__ == '__main__':
    app.run()
