from flask import Flask, request, render_template
import sqlite3, os, json
import random
import datetime
import re

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
          + "	SCORE INTEGER, TOTAL_TIME INTEGER, USED_TIME INTEGER," \
          + " START_TIME TIMESTAMP);"

    c.execute(sql)

    if category == '10':
        examType = 'FND(5問)'
    elif category == '20':
        examType = 'CDS(5問)'
    elif category == '30':
        examType = 'DSV(5問)'
    elif category == '40':
        examType = 'HVIT(5問)'
    elif category == '50':
        examType = 'DPI(5問)'
    elif category == '60':
        examType = '全体(10問)'
    elif category == '70':
        examType = '模擬試験(40問)'
    elif category == '80':
        examType = '修了試験(40問)'
    else:
        examType = 'その他'

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

NumOfArea = 5
NumOfCategory = 33
categoryCode = "0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW" \
               + "XYZ[]^`abcdefghijklmnopqrstuvwxyz"

categoryNumber = [11, 12, 13, 14, 15, 16, 17, \
                  21, 22, 23, 24, 25, \
                  31, 32, 33, 34, 35, 36, 37, 38, 39, \
                  41, 42, 43, 44, 45, 46, \
                  51, 52, 53, 54, 55, 56]


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

    NumOfCategory1=7
    NumOfCategory2=12
    NumOfCategory3=21
    NumOfCategory4=27
    NumOfCategory5=33
    NumOfCategory6=0

    arealist = ''
    for i in range(total):
        for j in range(NumOfCategory):
            #            print( 'categoryNumber[{0}])={1}'.format( j, categoryNumber[j]))
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
                else:
                    selectArea[5] += 1
#                elif (j < NumOfCategory6):
#                    selectArea[5] += 1
#                else:
#                    selectArea[6] += 1
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
        assign[0] = 15
        assign[1] = 12 + random.randint(0, 1)
        assign[2] = 16 + random.randint(0, 1)
        assign[3] = 11
        assign[4] = 14
    elif category == 20:
        assign[0] = 24
        assign[1] = 25
        assign[2] = 23
        assign[3] = 21
        assign[4] = 22
    elif category == 30:
        assign[0] = 36 + random.randint(0, 1)
        assign[1] = 31 + random.randint(0, 2)
        if assign[1] != 31:
            assign[1] = 32
        assign[2] = 34 + random.randint(0, 1)
        assign[3] = 38 + random.randint(0, 1)
        assign[4] = 33
    elif category == 40:
        assign[0] = 46
        assign[1] = 43 + random.randint(0, 1)
        assign[2] = 45
        assign[3] = 41 + random.randint(0, 1)
        assign[4] = 46
    elif category == 50:
        assign[0] = 53
        assign[1] = 55
        assign[2] = 51
        assign[3] = 56
        assign[4] = 52 + (random.randint(0, 1)*2)
    elif category == 60 or category == 70 or category == 80:
        assign[0] = 24    # バリューストリーム（ユーザサポート）
        assign[1] = 33    # デジタルサービス体験のデザイン
        assign[2] = 51    # コントロールの範囲の特定
        assign[3] = 45    # HVITにおける原則や概念
        assign[4] = 13    # 従うべき原則（個別）
        assign[5] = 39    # サービス価値の確認
        assign[6] = 17    # サービスバリューチェーン活動
        assign[7] = 21    # SVS導入における課題
        assign[8] = 56    # コミュニケーションの原則
        assign[9] = 41    # ＤX関連の概念
        if amount == 40:
            assign[10] = 36 + random.randint(0, 1)    # ユーザ・コミュニティ　& フィードバック管理
            assign[11] = 25                           # キューとバックログの管理
            assign[12] = 53                           # ガバナンス
            assign[13] = 46                           # HVITにおける原則や概念を支える行動
            assign[14] = 32 + random.randint(0, 1)    # エンゲージメント or 提案
            assign[15] = 11                           # サービス関係
            assign[16] = 55                           # 組織変更の管理
            assign[17] = 43                           # デジタル商品の５つの目標
            assign[18] = 38                           # 実現(DSV)
            assign[19] = 23                           # バリューストリーム（新サービス）
            assign[20] = 14                           # ４つの側面
            assign[21] = 54                           # コントロール(DPI)
            assign[22] = 22                           # SVS導入におけるリソース管理
            assign[23] = 46                           # HVITにおける原則や概念を支える行動
            assign[24] = 31                           # カスタマジャニー
            assign[25] = 21                           # SVS導入における課題
            assign[26] = 52                           # リスク管理(DPI)
            assign[27] = 42                           # DXに求められる環境と能力
            assign[28] = 12                           # 従うべき原則（全体）
            assign[29] = 24                           # バリューストリーム（ユーザ・サポート）
            assign[30] = 45                           # HVITにおける原則や概念
            assign[31] = 56                           # コミュニケーションの原則
            assign[32] = 51                           # コントロールの範囲の特定
            assign[33] = 34                           # オン/オフ・ボーディング
            assign[34] = 15                           # サービスバリューシステム
            assign[35] = 32                           # 関係タイプ
            assign[36] = 44                           # HVITとITILの関係
            assign[37] = 23                           # バリューストリーム（新サービス）
            assign[38] = 43                           # HVITにおける原則や概念を支える行動
            assign[39] = 35                           # オン/オフ・ボーディング
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



