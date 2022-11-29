import pandas as pd
import pymongo
from tqdm import tqdm

def main():
    data = pd.read_excel('./data/data.xlsx')
    data.rename(columns = {'도로명 기본주소' : '도로명기본주소'}, inplace = True)
    # connection
    connection = pymongo.MongoClient() # basic port : 27017
    # database instance화
    database = connection.database # database에 database가 없어도 자동 생성함.
    # db 이름 확인
    # collection
    leisure = database.corporations
    for i in tqdm(data.index, desc='make_db'):
        post_id = leisure.insert_one(data.loc[i,['시설종목명','시도명','시군구명','시설명','도로명기본주소','도로명상세주소','전화번호','홈페이지']].to_dict())
    print('done')
if __name__ == '__main__':
    main()