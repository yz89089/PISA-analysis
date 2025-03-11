import traceback

import pandas as pd
import sqlite3
from tqdm import trange
#%%
#处理学生层的数据，并存入数据库pisa31.db
#process student layer data and save it into pisa31.db

def trans_student2db2(isTest=False, start = 0):
    csv = pd.read_csv('student.csv', sep=',', encoding='utf8')
    #print(csv.head())
    if isTest:
        return
    print('Mission start')
    error_id = []
    with sqlite3.connect('pisa31.db') as conn:
        cursor = conn.cursor()
        cursor.execute('create table student(CNTSTUID int ,CNTSCHID int , CNTRYID int, gender int,ESCS float,gmc float,math2 float,math5 float, math9 float, read2 float, read5 float, read9 float, scie2 float,scie5 float,scie9 float) ')
        for j in trange(0, csv.shape[0]):
            try:
                gender = int(csv.loc[j]['ST004D01T']) - 1
                cursor.execute("insert into student (CNTSTUID, CNTSCHID, CNTRYID, gender,ESCS,gmc,math2,math5, math9, read2, read5, read9 ,scie2, scie5, scie9) values (?,?,?,?, ?,?,?,?, ?,?,?,? ,?,?,?)",
                            (int(csv.loc[j]['CNTSTUID']), int(csv.loc[j]['CNTSCHID']), int(csv.loc[j]['CNTRYID']),
                            gender, csv.loc[j]['ESCS'], float(csv.loc[j]['ST184Q01HA']),
                            float(csv.loc[j]['PV2READ']), float(csv.loc[j]['PV5READ']),float(csv.loc[j]['PV9READ']),
                            float(csv.loc[j]['PV2MATH']), float(csv.loc[j]['PV5MATH']),float(csv.loc[j]['PV9MATH']),
                            float(csv.loc[j]['PV2SCIE']), float(csv.loc[j]['PV5SCIE']),float(csv.loc[j]['PV9SCIE']),))
            
                
            
            except Exception:
                error_id.append(j)
                
            

        cursor.close()
        conn.commit()
        with open("error.txt", "a") as fh:
            fh.write("\n" + str(error_id))
    print('Mission finished')




if __name__ == '__main__':
    trans_student2db2()
    
