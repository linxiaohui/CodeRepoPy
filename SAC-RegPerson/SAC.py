# -*- coding: UTF-8 -*-
# 通过HTTP从证券业协会(SAC)下载 从业人员公示
# Last Update: 20190611
'''

'''
import time
import random
import sqlite3
import json
from datetime import datetime

import requests
import pandas as pd

DB_CONN = sqlite3.connect("sac_pro.db")
DB_CURSOR = DB_CONN.cursor()

#入口
PORTAL_URL = 'http://exam.sac.net.cn/pages/registration/sac-publicity-report.html'
#获取机构类型
INSTITUTION_TYPE_URL = 'http://exam.sac.net.cn/pages/registration/train-line-register!gsUDDIsearch.action'

HTTP_HEADERS = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Accept-Encoding":"gzip, deflate",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language":"zh-CN,zh;q=0.9"
}

sess = requests.Session()
HTTP_HEADERS['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
resp = sess.get(PORTAL_URL, headers=HTTP_HEADERS)

def sync_institution_type(sess):
    '''获取并返回机构类型'''
    global HTTP_HEADERS
    # 获取 机构类别
    HTTP_HEADERS['Referer'] = PORTAL_URL
    data = {
            'sqlkey': 'registration',
            'sqlval': 'ORG_TYPE_CODE'
           }
    resp = sess.post(INSTITUTION_TYPE_URL, data=data)
    institution_type = pd.read_json(resp.content, dtype=False)
    institution_type.to_sql("institution_type", DB_CONN, 
                        if_exists='replace', index=False)
    
    org_type = json.loads(resp.content)
    return org_type

def get_institution_by_type(ins_type, sess):
    '''根据机构类型获取机构列表'''
    global HTTP_HEADERS
    data = {
            'filter_EQS_OTC_ID': ins_type,
            'ORDERNAME': 'AOI#AOI_NAME',
            'ORDER': 'ASC',
            'sqlkey': 'registration',
            'sqlval': 'SELECT_LINE_PERSON'
           }
    INSTITUTION_LIST_URL = 'http://exam.sac.net.cn/pages/registration/train-line-register!orderSearch.action'
    resp = sess.post(INSTITUTION_LIST_URL, headers=HTTP_HEADERS, data=data)
    #目前不需要分页
    institutions = pd.read_json(resp.content, dtype=False)
    return institutions

def sync_institution(DB_CONN, sess):
    # 备份机构表
    try:
        today = datetime.now().strftime('%Y%m%d')
        DB_CONN.execute(f"ALTER TABLE institutions RENAME TO institutions_{today}")
        DB_CONN.execute(f"CREATE TABLE institutions AS SELECT * FROM institutions_{today} WHERE 0=1")
        DB_CONN.commit()
    except Exception as ex:
        DB_CONN.rollback()
        print(ex)
    
    org_type = sync_institution_type(sess)
    for t in org_type:
        otc_id = t['OTC_ID']
        institutions = get_institution_by_type(otc_id, sess)
        institutions['OTC_ID'] = t['OTC_ID']
        institutions['OTC_NAME'] = t['OTC_NAME']
        institutions['SYNC_STATUS'] = 0
        institutions.to_sql("institutions", DB_CONN, 
                            if_exists='append', index=False)

def get_persons_by_institution(aoi_id, sess):
    '''获取机构的人员'''
    global HTTP_HEADERS
    persons = []
    HTTP_HEADERS['Referer'] = f'http://exam.sac.net.cn/pages/registration/sac-publicity-finish.html?aoiId={aoi_id}'
    PERSON_URL = 'http://exam.sac.net.cn/pages/registration/train-line-register!list.action'
    pgno = 1
    data = {
            'filter_EQS_AOI_ID': aoi_id,
            'filter_EQS_PTI_ID': '',
            'page.searchFileName': 'homepage',
            'page.sqlKey': 'PAGE_FINISH_PUBLICITY',
            'page.sqlCKey': 'SIZE_FINISH_PUBLICITY',
            '_search': 'false',
            'nd': int(time.time()*1000),
            'page.pageSize': '100',
            'page.pageNo': 1,
            'page.orderBy': 'id',
            'page.order': 'desc'
            }
    while True:
        print(f"getting {aoi_id}. page {pgno}")
        data['page.pageNo'] = pgno
        data['nd'] = int(time.time()*1000)
        resp = sess.post(PERSON_URL, headers=HTTP_HEADERS, data=data)
        resp_json = json.loads(resp.content)
        persons.extend(resp_json['result'])
        if not resp_json['hasNext']:
            break
        pgno += 1
        time.sleep(2)
    return persons


def get_all_person_by_id(aoi_id, DB_CONN):
    exists = pd.read_sql(f"SELECT * FROM stuffs WHERE AOI_ID={aoi_id}", DB_CONN)
    return exists


def set_person_leave(aoi_id, cer_num, rpi_name, DB_CONN):
    DB_CONN.execute(f"UPDATE stuffs SET off_time = datetime('now','localtime')  WHERE AOI_ID={aoi_id} AND CER_NUM={cer_num} AND RPI_NAME={rpi_name}")

def set_person_info_ok(aoi_id, cer_num, rpi_name, DB_CONN):
    DB_CONN.execute(f"UPDATE stuffs SET status=1 WHERE AOI_ID={aoi_id} AND CER_NUM={cer_num} AND RPI_NAME={rpi_name}")

def sync_persons(persons, aoi_id, DB_CONN):
    '''同步机构人员'''
    # 现有人员信息
    exists = get_all_person_by_id(aoi_id, DB_CONN)
    exists_set = set()
    for k, row in exists.iterrows():
        cer_num, rpi_name = row[['CER_NUM','RPI_NAME']].tolist()
        exists_set.add((cer_num, rpi_name))       
        
    stuffs = pd.read_json(json.dumps(persons),dtype=False)
    stuffs['AOI_ID'] = aoi_id
    stuffs['REC_TIME'] = datetime.now()
    stuffs['OFF_TIME'] = None
    stuffs['STATUS'] = 0
    # 证书编号 CER_NUM 姓名 RPI_NAME
    # 对比获取新增人员、离职人员
    new_stuff = pd.DataFrame()
    now_stuff_set = set()
    for k, row in stuffs.iterrows():
        cer_num, rpi_name = row[['CER_NUM','RPI_NAME']].tolist()
        now_stuff_set.add((cer_num, rpi_name))
        if (cer_num, rpi_name) not in exists_set:
            new_stuff = new_stuff.append(row)
    # 更新数据库
    new_stuff.to_sql("stuffs", DB_CONN, 
                     if_exists='append', index=False)

    # 对之前存在目前不存在的人员，更新其OFF_TIME(为当前日期)
    leave_stuff = exists_set - now_stuff_set
    for cer_num, rpi_name in leave_stuff:
        set_person_leave(aoi_id, cer_num, rpi_name, DB_CONN)


def get_person_detail(ppp_id, aoi_id, DB_CONN, sess):
    global HTTP_HEADERS
    HTTP_HEADERS['Referer'] = f'http://exam.sac.net.cn/pages/registration/sac-finish-person.html?r2SS_IFjjk={ppp_id}'
    data = {'filter_EQS_PPP_ID': ppp_id,
            'sqlkey': 'registration',
            'sqlval': 'SD_A02Leiirkmuexe_b9ID'}
    RPI_ID_URL = 'http://exam.sac.net.cn/pages/registration/train-line-register!gsUDDIsearch.action'
    resp = sess.post(RPI_ID_URL, headers=HTTP_HEADERS, data=data)
    try:
        rpi_id = json.loads(resp.content)[0]['RPI_ID']
    except:
        print(json.loads(resp.content))
        raise
    data = {'filter_EQS_RPI_ID': rpi_id,
            'sqlkey': 'registration',
            'sqlval': 'SELECT_PERSON_INFO'}
    PERSON_INFO_URL = 'http://exam.sac.net.cn/pages/registration/train-line-register!gsUDDIsearch.action'
    resp = sess.post(PERSON_INFO_URL, headers=HTTP_HEADERS, data=data)
    person = json.loads(resp.content)
    person_info = pd.read_json(resp.content, dtype=False)
    person_info['IMAGE_DATA'] = None
    # 获取文件路径
    #FILE_PATH_URL = 'http://exam.sac.net.cn/pages/registration/train-line-register!resultFilePath.action'
    #data = {'fileType':'image'}
    #resp = sess.post(FILE_PATH_URL, headers=HTTP_HEADERS, data=data)
    FILE_BASE_URL = 'http://exam.sac.net.cn/photo/images/'
    if person[0]['RPI_PHOTO_PATH'] is not None:
        PIC_URL = FILE_BASE_URL + person[0]['RPI_PHOTO_PATH']
        resp = sess.get(PIC_URL)
        person_info['IMAGE_DATA'] = resp.content
    person_info.to_sql('person_info',DB_CONN, if_exists='append', index=False)

DB_CURSOR.execute("SELECT * FROM institutions WHERE sync_status!=2")
institution_to_sync = DB_CURSOR.fetchall()
for ins in institution_to_sync:
    print(ins)
    aoi_id = ins[0]
    sync_status = ins[-1]
    if sync_status==0:
        print("需要先同步人员信息")
        persons = get_persons_by_institution(aoi_id, sess)
        sync_persons(persons, aoi_id, DB_CONN)
        DB_CURSOR.execute(f"UPDATE institutions SET sync_status=1 WHERE aoi_id={aoi_id}")
        DB_CONN.commit()
    print("同步人员信息完成。下载详细信息...")
    # 同步人员详细信息
    DB_CURSOR.execute(f"SELECT * FROM stuffs WHERE aoi_id={aoi_id} AND status=0")
    person_to_sync = DB_CURSOR.fetchall()
    for p in person_to_sync:
        ppp_id = p[8]
        print(ppp_id, aoi_id)
        get_person_detail(ppp_id, aoi_id, DB_CONN, sess)
        DB_CURSOR.execute(f"UPDATE stuffs SET status=1 WHERE aoi_id={aoi_id} AND ppp_id='{ppp_id}'")
        DB_CONN.commit()
        time.sleep(int(3*random.random()+1))
    DB_CURSOR.execute(f"UPDATE institutions SET sync_status=2 WHERE aoi_id={aoi_id}")
    
    break