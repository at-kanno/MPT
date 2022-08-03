from flask import Flask, request, render_template
import sqlite3, os, json
import random
import datetime
import re
from constant import SECOND_TEST, ETYPE1, ETYPE2, ETYPE3, ETYPE4, ETYPE5, ETYPE6, \
    ETYPE7, ETYPE8, ETYPE9, ETYPE10, ETYPE11

DIFF_JST_FROM_UTC = 9

# データベースのパスを特定
base_path = os.path.dirname(os.path.abspath(__file__))
db_path = base_path + '/exam.sqlite'
form_path = base_path


class Question:
    def __init__(self, category, level, q, a1, a2, a3, a4, correct, cid):
        self.category = category
        self.level = level
        self.q = q
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.correct = correct
        self.cid = cid

    def show(self):
        print(f'質問 {self.q}')
        print(f'A. {self.a1}')
        print(f'B. {self.a2}')
        print(f'C. {self.a3}')
        print(f'D. {self.a4}')


class QuestionList:
    def __init__(self):
        self.data = []

    def add(self, question):
        self.data.append(question)

# 演習IDから問題を取得する
def getQuestion(examlist, q_no):

    print(examlist)
    s1 = examlist.strip('()')
    print(s1)
    s2 = s1.replace(')(', ',')
    print(s2)
    examlist2 = re.split('[:,]', s2)
    print(examlist2)

    number = examlist2[(q_no-1) * 5]
    idx = examlist2[(q_no-1)*5+1:(q_no) * 5]

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    q = Question

    sql = "SELECT Q,A1,A2,A3,A4,CID1 FROM knowledge_base WHERE NUMBER = " + str(number)
    c.execute(sql)
    items = c.fetchall()

    for k, r in enumerate(items):
        for s in range(4):
            if ((int(idx[s])) == 1):
                q.crct = s
        else:
            pass

    q.q = r[0]
    q.a1 = r[int(idx[0])]
    q.a2 = r[int(idx[1])]
    q.a3 = r[int(idx[2])]
    q.a4 = r[int(idx[3])]
    q.cid = r[5]

    print('Question=' + q.q)
    return q

# 演習IDから問題を取得する
def getQuestions(exam_id, qlist):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    q = Question
    #    qlist = QuestionList()

    sql = "SELECT  CDATE, CTIME, CATEGORY, LEVEL, AMOUNT," \
          + " EXAMLIST, AREALIST FROM EXAM_TABLE" \
          + " WHERE EXAM_ID = " + str(exam_id) + ";"

    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")

    items = c.fetchall()
    cdate = items[0][0]
    ctime = items[0][1]
    category = items[0][2]
    level = items[0][3]
    amount = items[0][4]
    examlist = items[0][5]
    arealist = items[0][6]

    print(examlist)
    s1 = examlist.strip('()')
    print(s1)
    s2 = s1.replace(')(', ',')
    print(s2)
    examlist2 = re.split('[:,]', s2)
    print(examlist2)

    idlist = examlist2[::5]
    idlistnum = len(idlist)
    idxlist = [['' for i in range(4)] for j in range(idlistnum)]
    for i in range(0, idlistnum):
        idxlist[i] = examlist2[i * 5 + 1:i * 5 + 5]
    print(idxlist[0])

    for j in range(0, idlistnum):
        sql = "SELECT Q,A1,A2,A3,A4,CID1 FROM knowledge_base WHERE NUMBER = " \
              + str(idlist[j])
        c.execute(sql)

        items = c.fetchall()

        for k, r in enumerate(items):
            for s in range(4):
                if ((int(idxlist[k][s])) == 1):
                    crct = s
                else:
                    pass

            q = Question(
                category, level, r[0],
                r[int(idxlist[k][0])],
                r[int(idxlist[k][1])],
                r[int(idxlist[k][2])],
                r[int(idxlist[k][3])],
                crct,
                r[5])
            print('Question=' + q.q)
            qlist[j] = q

    conn.close()

    return idlistnum


def getExamlist(exam_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    q = Question

    sql = "SELECT  CDATE, CTIME, CATEGORY, LEVEL, AMOUNT," \
          + " EXAMLIST, AREALIST FROM EXAM_TABLE" \
          + " WHERE EXAM_ID = " + str(exam_id) + ";"

    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")

    items = c.fetchall()
    cdate = items[0][0]
    ctime = items[0][1]
    category = items[0][2]
    level = items[0][3]
    amount = items[0][4]
    examlist = items[0][5]
    arealist = items[0][6]

    return examlist, arealist


def getExamCandidate(amount, category, level, mode):
    dt_now = datetime.datetime.now()
    condition = ""

    if (amount <= 0):
        return -1
    elif (amount > 40):
        return -1
    else:
        pass

    categoryStr = "CATEGORY = " + str(category)
    #    categoryStr = "CATEGORY >= " + str(category) + \
    #                  " AND CATEGORY < " + str(category+10)

    if (category != 0):
        condition = " WHERE " + categoryStr + " "
    # 出題領域とレベルの両方が指定されている場合
    #    if (level != 0):
    #        condition = str(condition) + " AND LEVEL = " + str(level)
    #    elif(level != 0):
    #        condition = " WHERE LEVEL = " + str(level)
    #    else :
    #        pass

    sql = "SELECT NUMBER FROM knowledge_base " + str(condition)

    # 無料の際の制限
    # if(mode==0 && (category != 100))
    #    sql = sql + "AND NUMBER < 66 ";
    print(sql)

    # データベースから値を取得
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(sql)
    items = c.fetchall()
    #    glist = [0 in range (30)]
    glist = []

    for i, r in enumerate(items):
        glist.append(r[0])
        print(str(glist))
    conn.close()

    print("候補数=" + str(len(glist)))
    print("要求数=" + str(amount))

    cnt = len(glist)
    index = []
    index = combination(cnt, amount)
    print('組み合わせ列={0}'.format(index))

    candidate = []
    for i in range(amount):
        candidate.append(glist[index[i]])
    return (candidate)


def combination(total, select):
    ns = []
    while len(ns) < select:
        n = random.randint(0, total - 1)
        print('n=' + str(n))
        if not n in ns:
            ns.append(n)
    return ns


def getCorrectList( examlist ):

    correctlist = ""
    s1 = examlist.strip('()')
    print(s1)
    s2 = s1.replace(')(', ',')
    print(s2)
    examlist2 = re.split('[:,]', s2)
    print(examlist2)
    for i,n in enumerate(examlist2):
        if i%5 == 0:
            cnt = 0
            continue
        else:
            cnt += 1
            if(n != '1'):
                continue
            else:
                correctlist = correctlist + str(cnt)
    return correctlist


def getQuestionFromCategory(start, end):

    items = [['' for i in range(100)] for j in range(6)]

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    q = Question

    sql = "SELECT Q,A1,A2,A3,A4,CID1,NUMBER FROM knowledge_base WHERE "\
            "CATEGORY >= " + str(start) + " AND CATEGORY <= " + str(end) + ";"

    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")

    items = c.fetchall()
    n = len(items)
    if n < 1:
        return False

# getQuestionFromCategory(11, 19)
# IndexError: list index out of range
    m = 0
    m = random.randint(1, n)
    q = items[m][0]

    permutation = GetRandom()
    a1 = items[m][permutation[0]]
    a2 = items[m][permutation[1]]
    a3 = items[m][permutation[2]]
    a4 = items[m][permutation[3]]
    perm = str(permutation[0]) + str(permutation[1]) + str(permutation[2]) + str(permutation[3])

    for i in range(4):
        if (permutation[i] == 1):
            crct = i
    cid = items[m][5]
    num = items[m][6]

    return q,a1,a2,a3,a4,crct,cid,num, perm

def getQuestionFromNum(number,permutation):

    items = [['' for i in range(1)] for j in range(6)]
    a = ['' for i in range(4)]

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    q = Question

    sql = "SELECT Q,A1,A2,A3,A4,CID1 FROM knowledge_base WHERE "\
            "NUMBER == " + str(number) + ";"

    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")

    items = c.fetchall()
    n = len(items)
    if n < 1:
        return False

    q = items[0][0]
    for i in range(4):
        idx = int(permutation[i])
        a[i] = items[0][idx]
    cid = items[0][5]

    return q,a[0],a[1],a[2],a[3],cid

def saveExam(user, category, level, amount, examlist, arealist):

    if os.name != 'nt':
        now = datetime.datetime.now() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
    else:
        now = datetime.datetime.now()

    cdate = now.strftime("%Y-%m-%d")
    ctime = now.strftime("%H:%M:%S")

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    #   演習テーブルを再構成したい場合
    sql = "DROP TABLE EXAM_TABLE;"
#    c.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS EXAM_TABLE (" \
          + " EXAM_ID INTEGER PRIMARY KEY AUTOINCREMENT," \
          + " USER_ID INTEGER, CDATE TIMESTAMP, CTIME TIMESTAMP," \
          + "	CATEGORY INTEGER, LEVEL INTEGER, AMOUNT INTEGER," \
          + " EXAMLIST LONG VARCHAR, AREALIST LONG VARCHAR," \
          + " RESULTLIST LONG VARCHAR,  EXAM_TYPE LONG VARCHAR," \
          + " SCORE INTEGER, RATE FLOAT, TOTAL_TIME INTEGER, USED_TIME INTEGER," \
          + " START_TIME TIMESTAMP);"

    c.execute(sql)

    if category == '10':
        examType = ETYPE1
    elif category == '20':
        examType = ETYPE2
    elif category == '30':
        examType = ETYPE3
    elif category == '40':
        examType = ETYPE4
    elif category == '50':
        examType = ETYPE5
    elif category == '60':
        examType = ETYPE6
    elif category == '70':
        examType = ETYPE7
    elif category == '80':
        examType = ETYPE8
    elif category == '85':
        examType = ETYPE9
    elif category == '86':
        examType = ETYPE10
    else:
        examType = ETYPE11

    sql = 'INSERT INTO EXAM_TABLE( USER_ID, CDATE, CTIME,'\
          + 'CATEGORY, LEVEL, AMOUNT, EXAMLIST, AREALIST, EXAM_TYPE ) VALUES ("'\
          + str(user) + '", "' + cdate + '" , "' + ctime + '" , ' \
          + str(category) + ', ' + str(level) + ', ' + str(amount) + ',"' \
          + examlist + '", "' + arealist + '", "' + examType + '");'

    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")
    conn.commit()

    sql = 'SELECT EXAM_ID FROM EXAM_TABLE WHERE USER_ID = ' \
          + str(user) + ' AND CDATE = "' + cdate + '" AND CTIME = "' + ctime + '";';

    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")
    items = c.fetchall()
    conn.close()

    print(items[0][0])
    return (items[0][0])


# 出題カテゴリから問題列を生成する
MaxQuestions = 40

NumOfArea = 8
NumOfCategory = 12

categoryCode = "0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"

categoryNumber = [11, 21, 31, 41, 51, 52, 53, 54, 55, 61, 71, 81]

def makeExam2(userid, amount, category: int, level, time, arealist):
    print('userid={0},amount={1}, category={2}, level={3},\
          time={4}, arealist={5}'.format(userid, amount, \
                                         category, level, time, arealist))
    list = [0 for i in range(MaxQuestions)]
    selectArea = [0 for i in range(NumOfArea)]
    selectCategory = [0 for i in range(NumOfCategory+1)]
    index = [0 for i in range(NumOfCategory+1)]
    genlist = [[0 for i in range(5)] for j in range(NumOfCategory+1)]

    total = amount;
    if total < 0 or total > MaxQuestions:
        return 0
    assign = [0 for i in range(MaxQuestions)]

    total = assignQuestions(total, assign, category)

    if total == -1:
        return 0

    print("Total:" + str(total))

# 選択された「エリア（領域）の個数」と「カテゴリの個数」を算出する
# それまでのカテゴリ数を加算する
    NumOfCategory1=1
    NumOfCategory2=2
    NumOfCategory3=3
    NumOfCategory4=4
    NumOfCategory5=9
    NumOfCategory6=10
    NumOfCategory7=11
    NumOfCategory8=12

    arealist = ''
    for i in range(total):
        for j in range(NumOfCategory):
            print( 'categoryNumber[{0}])={1}'.format( j, categoryNumber[j]))
            if (assign[i] == categoryNumber[j]):
                arealist = arealist + categoryCode[j]
                selectCategory[j] += 1
                print('arealist=' + arealist)

                if (j < NumOfCategory1):
                    selectArea[0] += 1
                elif (j < NumOfCategory2):
                    selectArea[1] += 1
                elif (j < NumOfCategory3):
                    selectArea[2] += 1
                elif (j < NumOfCategory4):
                    selectArea[3] += 1
                elif (j < NumOfCategory5):
                    selectArea[4] += 1
                elif (j < NumOfCategory6):
                    selectArea[5] += 1
                elif (j < NumOfCategory7):
                    selectArea[6] += 1
                elif (j < NumOfCategory8):
                    selectArea[7] += 1
                else:                    # ありえないデータ
                    selectArea[8] += 1
                break
            else:
                pass
    #        print('i={0}'.format(i))

    print('arealist=' + arealist)
    business_status = 0

    # ユーザーIDをチェックする（ログインいしているか、有料か無料か）

    for i in range(NumOfCategory):
        if (selectCategory[i]!=0):
            genlist[i] = getExamCandidate(selectCategory[i], categoryNumber[i], level, business_status)
        else:
            genlist[i] = '0'

    for i in range(total):
        j = categoryCode.find(arealist[i])
        list[i] = genlist[j][index[j]]
        index[j] += 1

    print('リスト={0}'.format(list))

    # デバッグ・コード：　演習ID（list[i]）が０なら、異常なので埋め合わせる
    #    if(list[i]==0):
    #        print("list[" + i + "]:" + list[i])
    #        print("*************** ERROR ****************\n")

    examlist = ""

    for i in range(amount):
        # 選択肢の配列を決定する
        permutation = GetRandom()
        print('permutation={0}'.format(permutation))

        examlist = examlist + "(" + str(list[i]) + ":" \
                   + str(permutation[0]) + "," + str(permutation[1]) + "," \
                   + str(permutation[2]) + "," + str(permutation[3]) + ")"

        print(examlist)

    return examlist, arealist


def GetRandom():
    data = [
        [1, 2, 3, 4],
        [1, 2, 4, 3],
        [1, 3, 2, 4],
        [1, 3, 4, 2],
        [1, 4, 2, 3],
        [1, 4, 3, 2],
        [2, 1, 3, 4],
        [2, 1, 4, 3],
        [2, 3, 1, 4],
        [2, 3, 4, 1],
        [2, 4, 1, 3],
        [2, 4, 3, 1],
        [3, 2, 1, 4],
        [3, 2, 4, 1],
        [3, 1, 2, 4],
        [3, 1, 4, 2],
        [3, 4, 2, 1],
        [3, 4, 1, 2],
        [4, 2, 3, 1],
        [4, 2, 1, 3],
        [4, 3, 2, 1],
        [4, 3, 1, 2],
        [4, 1, 2, 3],
        [4, 1, 3, 2],
    ]

    n = random.randint(0, 23)
    #    print(n)
    return data[n]

def assignQuestions(amount, assign, category:int):
    if (amount > MaxQuestions or amount < 0):
        return -1

# FND
    if category == 10:
        assign[0] = 11
        assign[1] = 11
        assign[2] = 11
        assign[3] = 11
        assign[4] = 11
    elif category == 20:
        assign[0] = 21
        assign[1] = 21
        assign[2] = 21
        assign[3] = 21
        assign[4] = 21
    elif category == 30:
        assign[0] = 31
        assign[1] = 31
        assign[2] = 31
        assign[3] = 31
        assign[4] = 31
    elif category == 40:
        assign[0] = 41
        assign[1] = 41
        assign[2] = 41
        assign[3] = 41
        assign[4] = 41
    elif category == 50:
        assign[0] = 54
        assign[1] = 52
        assign[2] = 55
        assign[3] = 51
        assign[4] = 53
    elif category == 60:
        assign[0] = 61
        assign[1] = 61
        assign[2] = 61
        assign[3] = 61
        assign[4] = 61
    elif category == 70:
        assign[0] = 71
        assign[1] = 71
        assign[2] = 81
        assign[3] = 71
        assign[4] = 71
    elif category == 80 or category == 85 or category == 86:
        assign[0] = 54    # サービスオペレーション
        assign[1] = 21    # サービスライフサイクル
        assign[2] = 51    # サービスストラテジ
        assign[3] = 31    # 一般的な概念と定義
        assign[4] = 55 + (random.randint(0, 1) * 26)   # 継続的サービス改善/技術とアーキテクチャ(55/81)
        assign[5] = 11    # プラクティスとしてのサービスマネジメント
        assign[6] = 52    # サービスデザイン
        assign[7] = 61 + (random.randint(0, 1) * 10)    # 機能/役割(61/71)
        assign[8] = 41    # 主要な原則とモデル
        assign[9] = 53    # サービストランジション
        if amount == 40:
            assign[10] = 31                           # 一般的な概念と定義
            assign[11] = 52                           # サービスデザイン
            assign[12] = 41                           # 主要な原則とモデル
            assign[13] = 11                           # プラクティスとしてのサービスマネジメント
            assign[14] = 54                           # サービスオペレーション
            assign[15] = 71                           # 役割
            assign[16] = 21                           # サービスライフサイクル
            assign[17] = 31                           # 一般的な概念と定義
            assign[18] = 53                           # サービストランジション
            assign[19] = 11                           # プラクティスとしてのサービスマネジメント
            assign[20] = 52                           # サービスデザイン
            assign[21] = 53 + random.randint(0, 1)    # サービスオペレーション(53/54)
            assign[22] = 31                           # 一般的な概念と定義
            assign[23] = 51                           # サービスストラテジ
            assign[24] = 21                           # サービスライフサイクル
            assign[25] = 41                           # 主要な原則とモデル
            assign[26] = 54                           # サービスオペレーション
            assign[27] = 11                           # プラクティスとしてのサービスマネジメント
            assign[28] = 52                           # サービスデザイン
            assign[29] = 31                           # 一般的な概念と定義
            assign[30] = 53                           # サービストランジション
            assign[31] = 55                           # 継続的サービス改善
            assign[32] = 52                           # サービスデザイン
            assign[33] = 61                           # 機能
            assign[34] = 41                           # 主要な原則とモデル
            assign[35] = 81                           # 技術とアーキテクチャ
            assign[36] = 54                           # サービスオペレーション
            assign[37] = 53                           # サービストランジション
            assign[38] = 31                           # 一般的な概念と定義
            assign[39] = 52                           # サービスデザイン
    else:
        print("Error!")
        return -1

    return amount

def stringToButton(s):
    if(s == ""):
        return ""
    if ',' in s:
        numlist = s.split(',')
        xxx = ""
        for i, m in enumerate(numlist):
            if '-' in m:
                n = m.lstrip('-')
                xxx = xxx + '<button type=submit style="color:red" name="command" value="' + n + '">' + n + '</button>'
            else:
                xxx = xxx + '<button type=submit style="color:black" name="command" value="' + m + '">' + m + '</button>'
        return xxx
    elif '-' in s:
        n = s.lstrip('-')
        return '<button type=submit style="color:red" name="command" value="' + n + '">' + n + '</button>'
    else:
        return '<button type=submit style="color:black" name="command" value="' + s + '">' + s + '</button>'



