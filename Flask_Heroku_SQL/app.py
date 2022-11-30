# create
import sqlite3
import pandas as pd
from tqdm import tqdm
from flask import Flask, render_template, request
def find_things(input:dict):
    con = sqlite3.connect('leisure221129.db')
    # create
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS LeisureDB(시설종목명 text, 시도명 text, 시군구명 text, 시설명 text, 도로명기본주소 text, 도로명상세주소 text, 전화번호 text, 홈페이지 text);")
    # cnt
    cur.execute('SELECT count(*) FROM LeisureDB')
    cnt = next(iter(cur))[0]
    if cnt == 0:
        data = pd.read_excel('./data/data.xlsx')
        data.rename(columns = {'도로명 기본주소' : '도로명기본주소'}, inplace = True)
        for i in tqdm(data.index, desc='make_db'):
            cur = con.cursor()
            dic =  data.loc[i,['시설종목명','시도명','시군구명','시설명','도로명기본주소','도로명상세주소','전화번호','홈페이지']].to_dict()
            cur.execute('INSERT INTO LeisureDB VALUES(:시설종목명, :시도명, :시군구명, :시설명, :도로명기본주소, :도로명상세주소, :전화번호, :홈페이지);',dic)
        con.commit()
    # search
    시설종목명 = input['시설종목명'].upper()
    시도명 = input['시도명']
    if 시설종목명 and 시도명:
        cur.execute("SELECT * FROM 'LeisureDB' WHERE 시설종목명 ='%s' AND 시도명 = '%s'"%(시설종목명,시도명))
    if 시설종목명 and not 시도명:
        cur.execute("SELECT * FROM 'LeisureDB' WHERE 시설종목명 ='%s'"%(시설종목명))
    if not 시설종목명 and 시도명:
        cur.execute("SELECT * FROM 'LeisureDB' WHERE 시도명 ='%s'"%(시도명))
    return cur    

app = Flask(__name__)
 
@app.route('/')
def inputTest(facility_type=None, location=None):
    return render_template('main_1.html', facility_type=facility_type, location=location)

@app.route('/find',methods=['POST'])
def find_corps(facility_type=None, location=None):
    if request.method == 'POST':
        facility_type = request.form['facility_type']
        location = request.form['location']
        if facility_type == 'none':
            facility_type = None
        if location == 'none':
            location = None
    else:
        facility_type = None
        location = None
        
    response = find_things(dict(시설종목명=facility_type,시도명=location))
    return render_template('main_2.html', data=response)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
