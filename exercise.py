from constant import db_path, PassScore1, PassScore2, categoryCode, practice, \
     NumOfArea, areaname, return1, return2, return3, return4
from constant import db_path
from flask import Flask, session, render_template, request, Blueprint
from users import getStage, setStage, getStatus
import sqlite3, os
import datetime
from examDB import getQuestion, getQuestions, Question, getCorrectList
from resultDB import putResult

exec_module = Blueprint("exercise", __name__, static_folder='./static')

# 問題の出題
@exec_module.route('/exercise')
def exercise():

    command = request.args.get("command", "")
    q_no = request.args.get("q_no", "")
    user_id = request.args.get("user_id", "")
    title = request.args.get("title", "")
    exam_id = request.args.get("exam_id", "")
    total = int(request.args.get("total", ""))
    examlist = request.args.get("examlist", "")
    arealist = request.args.get("arealist", "")
    m = request.args.get("timeMin", "")

    if m == '':
        timeMin = 0
    else:
        timeMin = int(request.args.get("timeMin", ""))
    s = request.args.get("timeSec", "")
    if s == '':
        timeSec = 0
    else:
        timeSec = int(request.args.get("timeSec", ""))

    stime = request.args.get("stime", "")
    Y = request.args.get("Y", "")

    stage = getStage(user_id)
    if (stage != 2 and stage != 3 and stage != 4):
        return render_template('error.html',
                               user_id=user_id,
                               error_message='エラーが発生しました。')
    if (stage == 2):
        setStage(user_id, 3)
    if (stage == 4):
        return render_template('error.html',
                               user_id=user_id,
                               error_message='試験が終了してから演習に戻ることはできません。ログインし直してください。')

    qlist = [0 for QuestionList in range(40)]
    selectStr = ["", "", "", ""]
    marklist = {"     "}
    backward = ""
    forward = ""

    if command == 'start':

        if os.name != 'nt':
            now = datetime.datetime.now() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
        else:
            now = datetime.datetime.now()

        stime = now.strftime("%H:%M:%S")
        sdate = now.strftime("%Y-%m-%d")
        stime = sdate + " " + stime

        q_no = 1
        q = Question
        q = getQuestion(examlist, q_no)

        backward = "disabled"
        answerlist = ""
        marklist = ""
        timeMin = 0
        timeSec = 0
        Y = 0

        for i in range(total):
            answerlist = answerlist + "0"
            marklist = marklist + "0"

        # データベースへ開始時間を格納
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        sql = 'UPDATE EXAM_TABLE SET START_TIME = "' + stime + '" WHERE EXAM_ID = ' + exam_id + ";"
        c.execute(sql)
        conn.commit()
        conn.close()

        return render_template('exercise.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               examlist=examlist,
                               arealist=arealist,
                               q_no=q_no,
                               question=q.q,
                               selection1=q.a1,
                               selection2=q.a2,
                               selection3=q.a3,
                               selection4=q.a4,
                               selectStr=selectStr,
                               marklist=marklist,
                               answerlist=answerlist,
                               backward=backward,
                               forward=forward,
                               timeMin=timeMin,
                               timeSec=timeSec,
                               title=title,
                               Y=Y,
                               )

    elif command == 'next':
        q_no = (int)(request.args.get("q_no", ""))
        marklist = request.args.get("marklist", "")
        answerlist = request.args.get("answerlist", "")

        q_no += 1
        q = getQuestion(examlist, q_no)

        if (q_no >= total):
            forward = "disabled"

        return render_template('exercise.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               examlist=examlist,
                               arealist=arealist,
                               q_no=q_no,
                               question=q.q,
                               selection1=q.a1,
                               selection2=q.a2,
                               selection3=q.a3,
                               selection4=q.a4,
                               selectStr=selectStr,
                               marklist=marklist,
                               answerlist=answerlist,
                               backward=backward,
                               forward=forward,
                               timeMin=timeMin,
                               timeSec=timeSec,
                               title=title,
                               Y=Y,
                               )

    elif command == 'previous':
        q_no = (int)(request.args.get("q_no", ""))
        marklist = request.args.get("marklist", "")
        answerlist = request.args.get("answerlist", "")

        q_no -= 1
        q = getQuestion(examlist, q_no)

        if (q_no == 1):
            backward = "disabled"

        return render_template('exercise.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               examlist=examlist,
                               arealist=arealist,
                               q_no=q_no,
                               question=q.q,
                               selection1=q.a1,
                               selection2=q.a2,
                               selection3=q.a3,
                               selection4=q.a4,
                               selectStr=selectStr,
                               marklist=marklist,
                               answerlist=answerlist,
                               backward=backward,
                               forward=forward,
                               timeMin=timeMin,
                               timeSec=timeSec,
                               title=title,
                               Y=Y,
                               )

    elif command == 'move':
        q_no = (int)(request.args.get("q_no", ""))
        marklist = request.args.get("marklist", "")
        answerlist = request.args.get("answerlist", "")

        q = getQuestion(examlist, q_no)

        if (q_no == 1):
            backward = "disabled"
        if (q_no == total):
            forward = "disabled"

        return render_template('exercise.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               examlist=examlist,
                               arealist=arealist,
                               q_no=q_no,
                               question=q.q,
                               selection1=q.a1,
                               selection2=q.a2,
                               selection3=q.a3,
                               selection4=q.a4,
                               selectStr=selectStr,
                               marklist=marklist,
                               answerlist=answerlist,
                               backward=backward,
                               forward=forward,
                               timeMin=timeMin,
                               timeSec=timeSec,
                               title=title,
                               Y=Y,
                               )

    elif (command == 'finish') or (command == 'timeout'):
        #   終了
        setStage(user_id, 4)
        answerlist = request.args.get("answerlist", "")
        examlist = request.args.get("examlist", "")
        correctlist = getCorrectList(examlist)
        correct = 0
        resultlist = ""
        for i, c in enumerate(answerlist):
            if (c == correctlist[i]):
                correct += 1
                resultlist = resultlist + "1"
            else:
                resultlist = resultlist + "0"

        # デバックのためのコード
        # 正解数を35にする
        # correct = 35

        # データベースへ試験結果を格納
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        rate = round((correct / total * 100), 1)
        usedTime = int(timeSec) + int(timeMin) * 60
        total_time = total * 90

        sql = "UPDATE EXAM_TABLE SET RESULTLIST = " + resultlist + ", SCORE = " + str(correct) + ", USED_TIME = " \
              + str(usedTime) + ", TOTAL_TIME = " + str(total_time) + ", RATE = " + str(rate) \
              + " WHERE EXAM_ID = " + exam_id + ";"
        print(sql)
        c.execute(sql)

        sql = "SELECT START_TIME, EXAM_TYPE FROM EXAM_TABLE WHERE EXAM_ID = " + exam_id + ";"
        c.execute(sql)
        items = c.fetchall()
        stime = items[0][0]
        type = items[0][1]
        conn.commit()
        conn.close()

        putResult(user_id, exam_id, total, arealist, answerlist, resultlist, correct, rate, usedTime)

        flag = 0
        old_status = getStatus(user_id)

        # ユーザのステータスを更新
        if rate >= PassScore2 and total == 40:
            status, flag = rankUp(user_id, 2)
        elif rate >= PassScore1 and total == 40:
            status, flag = rankUp(user_id, 1)

        if old_status == 31 and rate < PassScore2: # 75%を越えなければ、始めからやり直し
            rankDown(user_id)
            flag = 4
        if flag == 3:
            userInfo = ["", "", ""]
            userInfo = getMailadress(user_id)
            username = str(userInfo[0][0]) + " " + str(userInfo[0][1])
            to_email = str(userInfo[0][2])
            if old_status == 31:
                sendMail(username, to_email, "合格です。")

        if old_status >= 30 and type == '修了試験(40問)':
            if rate < PassScore2:
                if old_status >= 40:
                    message = "不合格でした。"
                else:
                    message = FAIL_MESSAGE
            elif old_status == 30:
                message = PASS1_MASSAGE
            elif old_status == 31:
                message = PASS2_MASSAGE
            else:
                message = "合格です。おめでとうございます。"

            return render_template('finish2.html',
                               user_id=user_id,
                               title=title,
                               message=message,
                               )
        else:
            return render_template('finish.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               examlist=examlist,
                               arealist=arealist,
                               answerlist=answerlist,
                               resultlist=resultlist,
                               correct=correct,
                               rate=rate,
                               timeMin=timeMin,
                               timeSec=timeSec,
                               stime=stime,
                               stage=stage,
                               title=title,
                               flag=flag,
                               )

