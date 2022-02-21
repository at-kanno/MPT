from flask import Flask, request, render_template
import sqlite3, os, json
import datetime
import re

# データベースのパスを特定
base_path = os.path.dirname(os.path.abspath(__file__))
db_path = base_path + '/exam.sqlite'
form_path = base_path

#SECOND_TEST = "修了試験"
SECOND_TETST = "実力確認試験"

NumOfArea = 7
NumOfCategory = 12
NumOfCategory1 = 3
NumOfCategory2 = 5
NumOfCategory3 = 6
NumOfCategory4 = 7
NumOfCategory5 = 9
NumOfCategory6 = 11
NumOfCategory7 = 12
NumOfCheckArea = 20

# 33だが、多めに設定している
categoryCode = "0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class ResultInfo:
    def __init__(self, user_id, exam_id, arealist, answerlist, resultlist):
        self.user_id = user_id
        self.exam_id = exam_id
        self.arealist = arealist
        self.answerlist = answerlist
        self.resultlist = resultlist

# 試験結果を格納する
def putResult(user_id, exam_id, amount, arealist, answerlist, resultlist, correct, rate, usedTime):
    categoryNumber = [0 for i in range(NumOfCategory)]
    categoryScore = [0 for i in range(NumOfCategory)]
    categoryPercent = [0 for i in range(NumOfCategory)]

    areaNumber = [0 for i in range(NumOfArea)]
    areaScore = [0 for i in range(NumOfArea)]
    areaPercent = [0 for i in range(NumOfArea)]

# ITIL 一般に関する出題
    for i, c in enumerate(arealist):
        if resultlist[i] == '1':
            flag = 1
        else:
            flag = 0
        n = categoryCode.find(c)
        categoryNumber[n] += 1
        categoryScore[n] = categoryScore[n] + flag
        if n < NumOfCategory1:
            areaNumber[0] += 1
            areaScore[0] = areaScore[0] + flag
        elif n < NumOfCategory2:
            areaNumber[1] += 1
            areaScore[1] = areaScore[1] + flag
        elif n < NumOfCategory3:
            areaNumber[2] += 1
            areaScore[2] = areaScore[2] + flag
        elif n < NumOfCategory4:
            areaNumber[3] += 1
            areaScore[3] = areaScore[3] + flag
        elif n < NumOfCategory5:
            areaNumber[4] += 1
            areaScore[4] = areaScore[4] + flag
        elif n < NumOfCategory6:
            areaNumber[5] += 1
            areaScore[5] = areaScore[5] + flag
        else:
            areaNumber[6] += 1
            areaScore[6] = areaScore[6] + flag

    for i in range(NumOfCategory):
        if categoryNumber[i] != 0:
            categoryPercent[i] = categoryScore[i] / categoryNumber[i] * 100

    for i in range(NumOfArea):
        if areaNumber[i] != 0:
            areaPercent[i] = areaScore[i] / areaNumber[i] * 100

    half1 = half2 = 0
    length =  round(len(resultlist)/2)
    for i in range(length):
        if resultlist[i] == '1' :
            half1 += 1
    for i in range(length,len(resultlist)):
        if resultlist[i] == '1':
            half2 += 1
    half1 = half1 / length * 100           # 正答率（前半）
    half2 = half2 / (len(resultlist) - length) * 100  # 正答率（後半）

    res = res_correct = 0

    for i, c in enumerate(answerlist):
        if c != '0' :
            res += 1                              # 解答数
    for i, c in enumerate(resultlist):
        if c == '1' :
            res_correct += 1                     # 正答数
    if res == 0:
        res_ratio = 0
    else:
        res_ratio = res_correct / res * 100          # 解答した問題に対する正答率
    total_time = amount * 90
    remain_time = total_time - usedTime          # 残り時間
    remain_time_rate = remain_time / total_time  # 残り時間の割合

    #    last3_answered                   # 最後の３問への解答数
    #    last3_result                     # 最後の３問の採点結果
    last3_answered = answerlist[-3:]
    last3_result = resultlist[-3:]
    last3 = 0
    for i, c in enumerate(last3_result):
        if c == '1':
            last3 += 1
    last3 = last3 / 3 * 100               # 最後の３問の正答率）

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = "DROP TABLE RESULT_TABLE;"
    # c.execute(sql)
    sql = "CREATE TABLE IF NOT EXISTS RESULT_TABLE ( EXAM_ID INTEGER, USER_ID INTEGER, EXAM_TYPE LONG VARCHAR,"\
        + "TOTAL INTEGER, TOTAL_R INTEGER, TOTAL_P FLOAT," \
        + "C1_NUMBER INTEGER, C1_SCORE INTEGER, C1_PERCENT FLOAT," \
        + "C2_NUMBER INTEGER, C2_SCORE INTEGER, C2_PERCENT FLOAT," \
        + "C3_NUMBER INTEGER, C3_SCORE INTEGER, C3_PERCENT FLOAT," \
        + "C4_NUMBER INTEGER, C4_SCORE INTEGER, C4_PERCENT FLOAT," \
        + "C5_NUMBER INTEGER, C5_SCORE INTEGER, C5_PERCENT FLOAT," \
        + "C6_NUMBER INTEGER, C6_SCORE INTEGER, C6_PERCENT FLOAT," \
        + "C7_NUMBER INTEGER, C7_SCORE INTEGER, C7_PERCENT FLOAT," \
        + "C8_NUMBER INTEGER, C8_SCORE INTEGER, C8_PERCENT FLOAT," \
        + "C9_NUMBER INTEGER, C9_SCORE INTEGER, C9_PERCENT FLOAT," \
        + "C10_NUMBER INTEGER, C10_SCORE INTEGER, C10_PERCENT FLOAT," \
        + "C11_NUMBER INTEGER, C11_SCORE INTEGER, C11_PERCENT FLOAT," \
        + "C12_NUMBER INTEGER, C12_SCORE INTEGER, C12_PERCENT FLOAT," \
        + "A1_NUMBER INTEGER, A1_SCORE INTEGER, A1_PERCENT FLOAT," \
        + "A2_NUMBER INTEGER, A2_SCORE INTEGER, A2_PERCENT FLOAT," \
        + "A3_NUMBER INTEGER, A3_SCORE INTEGER, A3_PERCENT FLOAT," \
        + "A4_NUMBER INTEGER, A4_SCORE INTEGER, A4_PERCENT FLOAT," \
        + "A5_NUMBER INTEGER, A5_SCORE INTEGER, A5_PERCENT FLOAT," \
        + "A6_NUMBER INTEGER, A6_SCORE INTEGER, A6_PERCENT FLOAT," \
        + "A7_NUMBER INTEGER, A7_SCORE INTEGER, A7_PERCENT FLOAT," \
        + "HALF1 FLOAT, HALF2 FLOAT, RESPONSE INTEGER, CORRECT_RES_RATE FLOAT," \
        + "REMAIN_TIME INTEGER, REMAIN_TIME_RATE FLOAT, LAST3 INTEGER);"
    c.execute(sql)

    sql = "INSERT INTO RESULT_TABLE( USER_ID, EXAM_ID, TOTAL, TOTAL_R, TOTAL_P ";
    for i in range(1,NumOfCategory+1):
        sql = sql + ", C"+ str(i) +"_NUMBER, C"+ str(i) +"_SCORE, C"+ str(i) +"_PERCENT";

    for i in range(1,NumOfArea+1):
        sql = sql + ", A" + str(i) + "_NUMBER, A" + str(i) + "_SCORE, A" + str(i) + "_PERCENT";

    sql = sql + ", HALF1, HALF2, RESPONSE, CORRECT_RES_RATE, REMAIN_TIME, REMAIN_TIME_RATE, LAST3" \
          + ") VALUES (" + str(user_id)  + ", " + str(exam_id) + ", " + str(amount) +", " + str(correct) +", " + str(rate) + " ";
    for i in range(NumOfCategory):
        sql = sql + ", " + str(categoryNumber[i]) + ", " + str(categoryScore[i]) + ", " + str(categoryPercent[i]);

    for i in range(NumOfArea):
        sql = sql + ", " + str(areaNumber[i]) + ", " + str(areaScore[i]) + ", " + str(areaPercent[i]);

    sql = sql + ", " + str(half1) + ", " + str(half2) + ", " + str(res) + ", " + str(res_ratio) + ", "\
          + str(remain_time) + ", " + str(remain_time_rate) + ", " + str(last3) + " )"

    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")
    conn.commit()

# 試験結果を抽出する
def getResult(exam_id):

    categoryNumber = [0 for i in range(NumOfCategory)]
    categoryScore = [0 for i in range(NumOfCategory)]
    categoryPercent = [0 for i in range(NumOfCategory)]

    areaNumber = [0 for i in range(NumOfArea)]
    areaScore = [0 for i in range(NumOfArea)]
    areaPercent = [0 for i in range(NumOfArea)]

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = "SELECT * FROM RESULT_TABLE WHERE EXAM_ID = " + str(exam_id) + ";"
    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")
    items = c.fetchall()
    user_id = items[0][1]
    total = items[0][3]
    correct = items[0][4]
    rate = items[0][5]

    for i in range(NumOfCategory):
        a = items[0][i * 3 + 6]
        b = items[0][i * 3 + 7]
        categoryNumber[i] = categoryNumber[i] + int(a)
        categoryScore[i] = categoryScore[i] + int(b)
        if categoryNumber[i] != 0:
            categoryPercent[i] = categoryScore[i] / categoryNumber[i] * 100

    for i in range(NumOfArea):
        areaNumber[i] = items[0][i*3+42]
        areaScore[i] = items[0][i*3+43]
        areaPercent[i] = items[0][i*3+44]

    return categoryNumber, categoryScore, categoryPercent, areaNumber, \
           areaScore, areaPercent

#   コメントIDからコメントを得る
def getComment(cid):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = "SELECT  COMMENT FROM COMMENTS_TABLE" \
          + " WHERE COMMENT_ID = " + str(cid) + ";"
    c.execute(sql)
    items = c.fetchall()
    conn.close()

    return items[0][0]

# コメント文を作成する
def makeComments(exam_id):

    categoryNumber = [0 for i in range(NumOfCategory)]
    categoryScore = [0 for i in range(NumOfCategory)]
    categoryPercent = [0 for i in range(NumOfCategory)]

    areaNumber = [0 for i in range(NumOfArea)]
    areaScore = [0 for i in range(NumOfArea)]
    areaPercent = [0 for i in range(NumOfArea)]

    result_data = [0 for i in range(9)]

    area, score, percent, user_id, half1, half2, res, correct_rate, \
    remain_time, remain_time_rate, last3 = getResultData(exam_id)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT TOTAL_TIME, USED_TIME, RESULTLIST, AREALIST, START_TIME'\
        ' FROM EXAM_TABLE WHERE EXAM_ID = ' + str(exam_id)
    c.execute(sql)
    items = c.fetchall()
    total_time = items[0][0]
    used_time = items[0][1]
    resultlist = items[0][2]
    arealist = items[0][3]
    start_time = items[0][4]

    sql = 'SELECT TOTAL, TOTAL_P, TOTAL_R,'\
          'A1_NUMBER, A1_SCORE, A1_PERCENT,'\
          'A2_NUMBER , A2_SCORE, A2_PERCENT,'\
          'A3_NUMBER , A3_SCORE , A3_PERCENT,'\
          'A4_NUMBER , A4_SCORE , A4_PERCENT,'\
          'A5_NUMBER , A5_SCORE , A5_PERCENT,'\
          'A6_NUMBER , A6_SCORE , A6_PERCENT,'\
          'A7_NUMBER , A7_SCORE , A7_PERCENT'\
          ' FROM RESULT_TABLE WHERE EXAM_ID = ' + str(exam_id)
    c.execute(sql)
    items = c.fetchall()

    total = items[0][0]
    total_p = items[0][1]
    total_r = items[0][2]

    for i in range(NumOfArea):
        areaNumber[i] = items[0][i*3+3]
        areaScore[i] = items[0][i*3+4]
        areaPercent[i] = items[0][i*3+5]

    sql = 'SELECT C1_NUMBER , C1_SCORE , C1_PERCENT,'\
          'C2_NUMBER , C2_SCORE , C2_PERCENT ,'\
          'C3_NUMBER , C3_SCORE , C3_PERCENT ,'\
          'C4_NUMBER , C4_SCORE , C4_PERCENT ,'\
          'C5_NUMBER , C5_SCORE , C5_PERCENT ,'\
          'C6_NUMBER , C6_SCORE , C6_PERCENT ,'\
          'C7_NUMBER , C7_SCORE , C7_PERCENT ,'\
          'C8_NUMBER , C8_SCORE , C8_PERCENT ,'\
          'C9_NUMBER , C9_SCORE , C9_PERCENT ,'\
          'C10_NUMBER , C10_SCORE , C10_PERCENT ,'\
          'C11_NUMBER , C11_SCORE , C11_PERCENT ,'\
          'C12_NUMBER , C12_SCORE , C12_PERCENT'\
          ' FROM RESULT_TABLE WHERE EXAM_ID = ' + str(exam_id)
    c.execute(sql)
    items = c.fetchall()

#
    for i in range(NumOfCategory):
        a = items[0][i * 3]
        b = items[0][i * 3 + 1]
        categoryNumber[i] = items[0][i*3]
        categoryScore[i] = items[0][i*3+1]
        categoryPercent[i] = items[0][i*3+2]

    weakArea = [0 for i in range(NumOfArea)]
    weakCategory = [0 for i in range(NumOfCategory)]
    weakAreaList1 = ""
    weakAreaList2 = ""
    weakCategoryList1 = ""
    weakCategoryList2 = ""

# カテゴリごとの正答率で、弱点を２段階（0点、50%以下）でリストする
    for i in range(NumOfCategory):
        if categoryNumber[i] != 0:
            if categoryPercent[i] == 0:
                weakCategory[i] = 1
                if( weakCategoryList1 != ""):
                    weakCategoryList1 = weakCategoryList1 + ',' + str(i)
                else:
                    weakCategoryList1 = weakCategoryList1 + str(i)
            elif categoryPercent[i] < 50:
                weakCategory[i] = 2
                if( weakCategoryList2 != ""):
                    weakCategoryList2 = weakCategoryList2 + ',' + str(i)
                else:
                    weakCategoryList2 = weakCategoryList2 + str(i)
            else:
                weakCategory[i] = 0

    n = 0
    for i in range(NumOfArea):
        if areaNumber[i] != 0:
            if areaPercent[i] == 0:
                weakArea[i] = 1
                n += 1
                weakAreaList1 = weakAreaList1 + str(i)
            elif areaPercent[i] < 50:
                weakArea[i] = 2
                weakAreaList2 = weakAreaList2 + str(i)
            else:
                weakArea[i] = 0

# 選択された領域を明かにする
    select = 0
    j = 0
    for i in range(NumOfArea):
        if areaNumber[i] != 0:
            j += 1
            select = i+1
# j = 1 でなければ、全領域を指定しているはず
    if j != 1:
        select = 0

    if total_p >= 90:
        cid =500
    elif total_p >= 75:
        cid = 501
    elif total_p >= 65:
        cid = 502
    elif total_p >= 40:
        cid = 503
    elif total_p >= 20:
        cid = 504
    elif correct_rate < 60:
        cid = 510
    else:
        cid = 505

#    conn = sqlite3.connect(db_path)
#    c = conn.cursor()

#    sql = "SELECT  COMMENT FROM COMMENTS_TABLE" \
#          + " WHERE COMMENT_ID = " + str(cid) + ";"
#    c.execute(sql)
#    items = c.fetchall()
#    comment = items[0][0] + "<br>"
    comment = "<br>" + getComment(cid) + "<br>"

# 残り時間の量で試験への取り組みを判別する
    if remain_time_rate > 0.5:
        cid = 511
        comment = comment + getComment(cid) + "<br>"
# 最後の３問の成績で試験への取り組みを判別する
    if last3 == 0:
        cid = 520
        comment = comment + getComment(cid) + "<br>"
# 前半と後半の成績の差で試験への取り組みを判別する
    if half1 - half2 > 50:
        cid = 521
        comment = comment + getComment(cid) + "<br>"
# 解答数をベースとした正答率で理解度を判別する
    if correct_rate >=85:
        cid = 514
        comment = comment + getComment(cid) + "<br>"
    elif correct_rate > 70:
        cid = 513
        comment = comment + getComment(cid) + "<br>"

    if correct_rate < 30:
        cid = 512
        comment = comment + getComment(cid) + "<br>"

#   解答結果の分析とコメント選択
#   全領域選択の場合
    if total == 40 or total == 10:
#   すべての領域で 50 % 以下の正答率の場合
        if areaPercent[0] < 50 and areaPercent[1] < 50 and areaPercent[2] < 50 \
                and areaPercent[3] < 50 and areaPercent[4] :
            cid = 538
#   全領域で 80 % 以上、正解している場合
        elif areaPercent[0] > 80 and areaPercent[1] > 80 and areaPercent[2] > 80\
                and areaPercent[3] > 80 and areaPercent[4] > 80:
            cid = 590
#   50 % 以下の正答率の領域があった場合
        elif areaPercent[0] < 50 or areaPercent[1] < 50 or areaPercent[2] < 50\
                or areaPercent[3] or areaPercent[4] :
#   かつ、80 % 以上の正答率の領域もある場合
            if areaPercent[0] > 80 or areaPercent[1] > 80 or areaPercent[2] > 80\
                or areaPercent[3] > 80 or areaPercent[4] > 80:
                cid = 591
#   かつ、80 % 　以上正答した領域がない場合
            else:
                cid = 537
#   すべての領域が 50 % 以上の正答率であり、80 % を超える領域もある場合
        elif areaPercent[0] > 80 or areaPercent[1] > 80 or areaPercent[2] > 80\
                or areaPercent[3] > 80 or areaPercent[4] > 80 :
            cid = 592
# すべての領域が 50 % 以上、79 % 以下の正答率である場合
        else:
            cid = 594
#   各領域の正答率から判断した分析結果をコメントする
        comment = comment + getComment(cid) + "<br><br>"

#   弱点を指摘する
        list = ""
        if (cid == 537 or cid == 538 or cid == 591) and n != 0:

            j = 0
            for i, n in enumerate(weakArea) :
                if n == 1:
                    if j != 0:
                        list = list + '、'
                    list = list + '「' + getComment(750 + i) + '」'
                    j += 1
            list = list + getComment(539)
        comment = comment + list
        comment = comment + "<BR>"

#   出題領域を選択している場合
    else:
        if select != 0 :
            cid = 700 + select
            comment = comment + '「' + getComment(cid) + '」'
            cid = 589
            comment = comment + getComment(cid) + "<BR>"

        #   不得意領域を指摘する
        m = 0
        list = ""
        for i in range(NumOfCategory-1):
            if weakCategory[i] == 1:
                if m != 0:
                    list = list + "、"
                m = m + 1
                list = list + '「' + getComment(750 + i) + '」'
        #   不得意領域がない場合
        if m == 0:
            cid = 595
            comment = comment + getComment(cid)
        else:
            comment = comment + list + getComment(539)
    comment = comment + "<BR>"
    return comment

def getResultData(exam_id):

    area = [0 for i in range(48)]
    score = [0 for i in range(48)]
    percent = [0 for i in range(48)]

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = "SELECT * FROM RESULT_TABLE WHERE EXAM_ID = " + str(exam_id)
    c.execute(sql)
    items = c.fetchall()

    user_id = items[0][1]
    area[45] = items[0][3]
    score[45] = items[0][4]
    percent[45] = items[0][5]
    for i in range(19):
        area[i]= items[0][i*3+6]
        score[i]= items[0][i*3+7]
        percent[i]= items[0][i*3+8]
    half1 = items[0][63]
    half2 = items[0][64]
    res = items[0][65]
    correct_rate = items[0][66]
    remain_time = items[0][67]
    remain_time_rate = items[0][68]
    last3 = items[0][69]

    conn.close()
    return area, score, percent, user_id, half1, half2, res, correct_rate, \
           remain_time, remain_time_rate, last3

def getUserResultList(user_id):

    n = 0
    userlist = []
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT USER_TABLE.LASTNAME, RESULT_TABLE.TOTAL, RESULT_TABLE.TOTAL_R,'\
       'RESULT_TABLE.TOTAL_P, EXAM_TABLE.START_TIME, EXAM_TABLE.EXAM_TYPE, '\
       'USER_TABLE.MAIL_ADR FROM RESULT_TABLE INNER JOIN EXAM_TABLE ON '\
       'RESULT_TABLE.EXAM_ID = EXAM_TABLE.EXAM_ID JOIN USER_TABLE ON '\
       'RESULT_TABLE.USER_ID = USER_TABLE.USER_ID '

#    sql = 'SELECT RESULT_TABLE.EXAM_ID, RESULT_TABLE.TOTAL, RESULT_TABLE.TOTAL_R,'\
#       'RESULT_TABLE.TOTAL_P, EXAM_TABLE.START_TIME, EXAM_TABLE.EXAM_TYPE '\
#       'FROM RESULT_TABLE INNER JOIN EXAM_TABLE ON '\
#       'RESULT_TABLE.EXAM_ID = EXAM_TABLE.EXAM_ID '
#    if user_id > '3':
    sql = sql + 'where RESULT_TABLE.USER_ID = ' + str(user_id) + \
          ' AND EXAM_TABLE.EXAM_TYPE != ' + SECOND_TEST + '(40問)'
    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        # 結果を入手
#        res = []
#        for i, r in enumerate(items):
#            user_id, name, mail_adr = (r[0], r[1], r[2])
#            userlist.append(user_id,name,mail_adr)

        conn.close()
        return items, n
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False, n


def getStartTime(exam_id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT START_TIME FROM EXAM_TABLE where EXAM_ID = ' + str(exam_id)
    try:
        c.execute(sql)
        items = c.fetchall()

        conn.close()
        return items[0][0]
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getUserResultList1(user_id):

    userlist = []
    n = 0
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT USER_TABLE.LASTNAME, USER_TABLE.STATUS, RESULT_TABLE.TOTAL, RESULT_TABLE.TOTAL_R,'\
       'RESULT_TABLE.TOTAL_P, EXAM_TABLE.START_TIME, EXAM_TABLE.EXAM_TYPE, '\
       'USER_TABLE.MAIL_ADR FROM RESULT_TABLE INNER JOIN EXAM_TABLE ON '\
       'RESULT_TABLE.EXAM_ID = EXAM_TABLE.EXAM_ID JOIN USER_TABLE ON '\
       'RESULT_TABLE.USER_ID = USER_TABLE.USER_ID '

    sql = sql + 'where RESULT_TABLE.USER_ID = ' + str(user_id) \
          + ' AND (EXAM_TABLE.EXAM_TYPE = "模擬試験(40問)") '
    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        conn.close()
        return items, n
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False, n

def getUserResultList2(user_id):

    n = 0
    userlist = []
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT USER_TABLE.LASTNAME, USER_TABLE.STATUS, '\
       'RESULT_TABLE.TOTAL_P, EXAM_TABLE.START_TIME, EXAM_TABLE.EXAM_TYPE, '\
       'USER_TABLE.MAIL_ADR FROM RESULT_TABLE INNER JOIN EXAM_TABLE ON '\
       'RESULT_TABLE.EXAM_ID = EXAM_TABLE.EXAM_ID JOIN USER_TABLE ON '\
       'RESULT_TABLE.USER_ID = USER_TABLE.USER_ID '

    sql = sql + 'where RESULT_TABLE.USER_ID = ' + str(user_id) \
          + ' AND (EXAM_TABLE.EXAM_TYPE = "' + SECOND_TEST + '(40問)") '
    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        conn.close()
        return items, n
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False, n
