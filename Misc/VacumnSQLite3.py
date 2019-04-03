#-*- coding:UTF-8 -*-
'''
'''
import sys
import os
import sqlite3

SOURCE_DB = sys.argv[1]
DESTN_DB = sys.argv[2]

print(SOURCE_DB)
print(DESTN_DB)

SOURCE_CONN = sqlite3.connect(SOURCE_DB)
DESTN_CONN = sqlite3.connect(DESTN_DB)

i=0
for sql in SOURCE_CONN.iterdump():
    i+=1
    if i%100==0:
        DEST_CONN.commit()
        print(i)
    DESTN_CONN.execute(sql)

DEST_CONN.commit()
