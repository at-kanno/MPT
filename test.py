from constant import db_path
import sqlite3
from flask import Flask, render_template

def setGrade(grade):

    sql = 'INSERT INTO RESULT_TABLE VALUES('\
        + '64,15,NULL,40,32,80.0,1,1,100.0,1,1,100.0,1,1,100.0,'\
        + '1,1,100.0,1,1,100.0,0,0,0.0,1,1,100.0,2,1,50.0,1,0,0.0,'\
        + '2,2,100.0,2,2,100.0,1,1,100.0,1,0,0.0,1,0,0.0,2,2,100.0,'\
        + '1,1,100.0,1,1,100.0,0,0,0.0,1,1,100.0,1,1,100.0,1,1,100.0,'\
        + '1,1,100.0,1,1,100.0,2,1,50.0,1,1,100.0,2,2,100.0,2,1,50.0,'\
        + '2,1,50.0,1,0,0.0,1,1,100.0,1,1,100.0,1,1,100.0,2,2,100.0,'\
        + 'NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'\
        + '6,6,100.0,8,6,75.0,9,7,77.777777777777785672,9,7,77.777777777777785672,8,6,75.0,'\
        + 'NULL,NULL,NULL,NULL,NULL,NULL,85.0,75.0,40,80.0,284,0.078888888888888883399,'\
        + '66.666666666666657193);'

    user_id = 13

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'UPDATE USER_TABLE SET STATUS = ' + str(grade) + \
          ' WHERE USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        conn.commit()
    except:
        conn.close()
        return render_template('error.html',
                               user_id=user_id,
                               error_message='失敗しました。',
                               )
    conn.close()
    return render_template('success.html',
                           user_id=user_id,
                           message='成功しました。',
                           )


