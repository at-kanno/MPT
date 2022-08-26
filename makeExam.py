from constant import db_path
from flask import Flask, session, render_template, request, Blueprint
import sqlite3, os
from users import getStage, setStage, getStatus
from examDB import makeExam2, getQuestionFromCategory, getQuestionFromNum, saveExam, getCorrectList

exam_module = Blueprint("exam", __name__, static_folder='./static')

# 基本概念を選択
@exam_module.route('/makeExam', methods=['POST'])
def makeExam():
    user_id = request.form.get('user_id')
    stage = getStage(user_id)
    #    if(stage != 1 and stage !=2):
    #        return """
    #        <h1>異常を検出しました。<br>
    #        ログインし直してください。</h1>
    #        <p><a href="/">→ログインする</a></p>
    #        """
    if (stage == 1):
        setStage(user_id, 2)

    if not is_login():
        return """
        <h1>ログインしてください</h1>
        <p><a href="/">→ログインする</a></p>
        """
    if request.method == 'POST':
        category = request.form['category']
        print('category=' + str(category))

        level = 1
        if (category == '01'):
            status = getStatus(user_id)
            return render_template('main-menu.html',
                                   user_id=user_id,
                                   status=status,
                                   )
        elif (category == '60'):
            amount = 10
            title = '確認問題（全領域）'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 900, '')
        elif (category == '70'):
            amount = 40
            title = '模擬試験'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 3600, '')
        elif (category == '80'):
            amount = 40
            title = '修了試験'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 3600, '')
        elif (category == '10'):
            amount = 5
            title = 'FND：確認問題'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 450, '')
        elif (category == '20'):
            amount = 5
            title = 'CDS：確認問題'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 450, '')
        elif (category == '30'):
            amount = 5
            title = 'DSV：確認問題'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 450, '')
        elif (category == '40'):
            amount = 5
            title = 'HVIT：確認問題'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 450, '')
        elif (category == '50'):
            amount = 5
            title = 'DPI：確認問題'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 450, '')
        elif (category == '91' or category == '92' or category == '93' \
              or category == '94' or category == '95'):
            amount = 5
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 450, '')
        else:
            setStage(user_id, 9)
            return render_template('admin.html', user_id=int(user_id))
        try:
            exam_id = saveExam(user_id, category, level, amount, examlist, arealist)
            # for debug
            correctlist = getCorrectList(examlist)
            return render_template('startExam.html',
                                   user_id=user_id,
                                   exam_id=exam_id,
                                   total=amount,
                                   examlist=examlist,
                                   arealist=arealist,
                                   title=title,
                                   correctlist=correctlist,
                                   )
        except:
            return "Error...."
    else:
        return 'Fail'


# 基本概念を選択
@exam_module.route('/makeExam3', methods=['POST'])
def makeExam3():

    user_id = request.form.get('user_id')
    command = request.form.get('command')

    if command == 'exit':
        status = getStatus(user_id)
        return render_template('main-menu.html',
                               user_id=user_id,
                               status=status,
                               )

    category = request.form['category']

    if command == 'check' or command == 'timeout':
        crct = int(request.form.get('crct'))
        num = request.form.get('num')
        ans = int(request.form.get('answer'))
        cid = request.form.get('cid')
        permutation = request.form.get('permutation')
        if ans == 9:
            correct = '選択がなされませんでした。'
        elif ans - 1 == crct:
            correct = '正解です。'
        else:
            correct = '誤りです。'

        q, a1, a2, a3, a4, cid = getQuestionFromNum(num, permutation)

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        sql = "SELECT  COMMENT FROM COMMENTS_TABLE" \
              + " WHERE COMMENT_ID = " + str(cid) + ";"
        if c.execute(sql):
            print("Success!")
        else:
            print("Error!")
        items = c.fetchall()
        comment = items[0][0]

        area = request.form.get('area')
        return render_template('analysis2.html',
                               user_id=user_id,
                               q=q,
                               a1=a1,
                               a2=a2,
                               a3=a3,
                               a4=a4,
                               correct=correct,
                               comment=comment,
                               answer="ABCD"[crct],
                               category=category,
                               area=area,
                               )
    else:
        stage = getStage(user_id)
        if (stage == 1):
            setStage(user_id, 2)

        if not is_login():
            return """
            <h1>ログインしてください</h1>
            <p><a href="/">→ログインする</a></p>
            """

        #        category = request.form['category']
        print('category=' + str(category))

        if (category == '91'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(11, 19)
        elif (category == '92'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(21, 29)
        elif (category == '93'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(31, 39)
        elif (category == '94'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(41, 49)
        elif (category == '95'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(51, 59)
        else:
            setStage(user_id, 1)
            status = getStatus(user_id)
            return render_template('main-menu.html',
                                   user_id=user_id,
                                   status=status,
                                   )

    area = ['FND', 'CDS', 'DSV', 'HVIT', 'DPI']
    n = int(category) - 91
    return render_template('exercise2.html',
                           user_id=user_id,
                           question=q,
                           selection1=a1,
                           selection2=a2,
                           selection3=a3,
                           selection4=a4,
                           timeMin=0,
                           timeSec=0,
                           selectStr="",
                           crct=crct,
                           cid=cid,
                           num=num,
                           permutation=permutation,
                           category=category,
                           area=area[n]
                           )

# ログインしているか調べる
@exam_module.route('/is_login')
def is_login():
    if 'login' in session:
        return "on"
    else:
        return "off"
    return 'login' in session