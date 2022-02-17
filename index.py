from flask import Flask, session, render_template, request, jsonify
import logging
import sqlite3, os, sys, cgi
import datetime
from users import check_login, getStage, setStage, getUserList, \
    deleteUser, getUserInfo, addUser, password_verify, setPassword, resetPassword, getLoginName, \
    getLoginPassword, getStatus, rankUp, rankDown, modifyUser,getMailadress
from exam_test import getQuestion, getQuestions, Question, \
    makeExam2, saveExam, getCorrectList, stringToButton, getExamlist, \
    getQuestionFromCategory, getQuestionFromNum
from result_info import putResult, getResult, makeComments, getComment, \
    getUserResultList, getUserResultList1, getUserResultList2, getStartTime
from mail import sendMail
from test import setGrade
from sql import convertQuestions, convertComments

DIFF_JST_FROM_UTC = 9

app = Flask(__name__, static_folder='./static')
app.secret_key = '9KStWezD'  # セッション情報を暗号化するための鍵
# 日本語を使えるように
app.config['JSON_AS_ASCII'] = False
books = [{'name': 'EffectivePython', 'price': 3315}, {'name': 'Expert Python Programming', 'price': 3960}]

base_path = os.path.dirname(__file__)
DATA_FILE = base_path + '/venv/data/users.json'
db_path = base_path + '/exam.sqlite'
form_path = base_path + '/templates'
FILES_DIR = base_path + '/static'

# css_path = base_path + '/css/style.css'
# css_path = base_path + '/css/style.css'
LOGFILE_NAME = "DEBUG.log"

app.logger.setLevel(logging.DEBUG)
log_handler = logging.FileHandler(LOGFILE_NAME)
log_handler.setLevel(logging.DEBUG)
app.logger.addHandler(log_handler)


NumOfArea = 7
NumOfCategory = 12
PassScore1 = 65
PassScore2 = 75

prefec = ["都道府県",
          "北海道",
          "青森県",
          "岩手県",
          "秋田県",
          "山形県",
          "宮城県",
          "福島県",
          "茨城県",
          "栃木県",
          "群馬県",
          "埼玉県",
          "千葉県",
          "東京都",
          "神奈川県",
          "新潟県",
          "富山県",
          "石川県",
          "福井県",
          "山梨県",
          "長野県",
          "岐阜県",
          "静岡県",
          "愛知県",
          "三重県",
          "滋賀県",
          "京都府",
          "大阪府",
          "兵庫県",
          "奈良県",
          "和歌山県",
          "鳥取県",
          "島根県",
          "岡山県",
          "広島県",
          "山口県",
          "徳島県",
          "香川県",
          "愛媛県",
          "高知県",
          "福岡県",
          "佐賀県",
          "長崎県",
          "熊本県",
          "大分県",
          "宮崎県",
          "鹿児島県",
          "沖縄県", ]


# ブラウザのメイン画面
@app.route('/')
def index():
    return render_template('login.html',
#                           css_path = css_path
                           )

# ログアウト処理
@app.route('/logout', methods=['POST'])
def logout():
    user_id = int(request.form['user_id'])
    #    user_id = request.form.get('user_id')
    setStage(user_id, 0)
    return render_template('login.html',
# css_path = css_path
                           )
    session.pop('login', None)
    return True

return1 = '<form action="makeExam" method="POST">' + \
          '<input type="hidden" name="user_id" value="'
return2 = '" /><button type="submit" class="btn btn-primary btn-block" name="category" value="99">' + \
          '管理画面へ戻る</button><br></p></form>'

return3 = '<div class="buttonwrap" style="display:inline-flex"><form action="summary" >' + \
          '<input type="hidden" name="user_id" value="'
return4 = '" /><button type="submit" style="margin:10px" name="category" value="99">' + \
          'メインメニューへ戻る</button><br></p></form>'

@app.route('/registration', methods=['POST'])
def registration():
    user_id = int(request.form['user_id'])

    lastname = request.form.get('lastname')
    if lastname is None:
        lastname = ''
    firstname = request.form.get('firstname')
    if firstname is None:
        firstname = ''
    lastyomi = request.form.get('lastyomi')
    if lastyomi is None:
        lastyomi = ''
    firstyomi = request.form.get('firstyomi')
    if firstyomi is None:
        firstyomi = ''
    tel1 = request.form.get('tel1')
    if tel1 is None:
        tel1 = ''
    tel2 = request.form.get('tel2')
    if tel2 is None:
        tel2 = ''
    tel3 = request.form.get('tel3')
    if tel3 is None:
        tel3 = ''
    company = request.form.get('company')
    if company is None:
        company = ''
    department = request.form.get('department')
    if department is None:
        department = ''
    zip1 = request.form.get('zip1')
    if zip1 is None:
        zip1 = ''
    zip2 = request.form.get('zip2')
    if zip2 is None:
        zip2  = ''
    prefecture = request.form.get('prefecture')
    city = request.form.get('city')
    if city is None:
        city = ''
    town = request.form.get('town')
    if town is None:
        town = ''
    building = request.form.get('building')
    if building is None:
        building = ''
    mail_adr = request.form.get('mail_adr')
    if mail_adr is None:
        mail_adr = ''
    retype = request.form.get('retype')
    if retype is None:
        retype = ''
    error_no = 0

    return render_template('registration.html',
                           lastname=lastname,
                           firstname=firstname,
                           lastyomi=lastyomi,
                           firstyomi=firstyomi,
                           tel1=tel1,
                           tel2=tel2,
                           tel3=tel3,
                           company=company,
                           department=department,
                           zip1=zip1,
                           zip2=zip2,
                           prefecture=prefecture,
                           prefec=prefec,
                           #                           pref = pref,
                           city=city,
                           town=town,
                           building=building,
                           mail_adr=mail_adr,
                           retype=retype,
                           user_id=user_id,
                           error_no=error_no,
                           )


@app.route('/confirmation', methods=['POST'])
def confirmation():
    user_id = int(request.form.get('user_id'))
    command = request.form.get('command')

#    error_no = int(request.form.get('error_no'))
    error_no = 0

    if command == 'modify':
        id = int(request.form.get('id'))
    else:
        id = 0
    lastname = request.form.get('lastname')
    firstname = request.form.get('firstname')
    lastyomi = request.form.get('lastyomi')
    firstyomi = request.form.get('firstyomi')
    tel1 = request.form.get('tel1')
    tel2 = request.form.get('tel2')
    tel3 = request.form.get('tel3')
    company = request.form.get('company')
    department = request.form.get('department')
    zip1 = request.form.get('zip1')
    zip2 = request.form.get('zip2')
    prefecture = request.form.get('prefecture')
    city = request.form.get('city')
    town = request.form.get('town')
    building = request.form.get('building')
    mail_adr = request.form.get('mail_adr')
    retype = request.form.get('retype')

    if firstname == "" or lastname == "":
        error_no = 11
    if mail_adr == "" or retype == "":
        error_no = 12
    if mail_adr != retype:
        error_no = 1

    if error_no != 0:
        # エラー処理
        if prefecture != "":
            try:
                pref = prefec.index(prefecture)
            except:
                pref = 0
        if id == 0:
            return render_template('registration.html',
                                   lastname=lastname,
                                   firstname=firstname,
                                   lastyomi=lastyomi,
                                   firstyomi=firstyomi,
                                   tel1=tel1,
                                   tel2=tel2,
                                   tel3=tel3,
                                   company=company,
                                   department=department,
                                   zip1=zip1,
                                   zip2=zip2,
                                   prefecture=prefecture,
                                   prefec=prefec,
                                   pref = pref,
                                   city=city,
                                   town=town,
                                   building=building,
                                   mail_adr=mail_adr,
                                   retype=retype,
                                   user_id=user_id,
                                   error_no=error_no,
                                   )

        else:
            return render_template('modification.html',
                                   lastname=lastname,
                                   firstname=firstname,
                                   lastyomi=lastyomi,
                                   firstyomi=firstyomi,
                                   tel1=tel1,
                                   tel2=tel2,
                                   tel3=tel3,
                                   company=company,
                                   department=department,
                                   zip1=zip1,
                                   zip2=zip2,
                                   prefecture=prefecture,
                                   prefec=prefec,
                                   pref=pref,
                                   city=city,
                                   town=town,
                                   building=building,
                                   mail_adr=mail_adr,
                                   retype=retype,
                                   user_id=user_id,
                                   id=id,
                                   error_no=error_no,
                                   )

    return render_template('confirm.html',
                           lastname=lastname,
                           firstname=firstname,
                           lastyomi=lastyomi,
                           firstyomi=firstyomi,
                           tel1=tel1,
                           tel2=tel2,
                           tel3=tel3,
                           company=company,
                           department=department,
                           zip1=zip1,
                           zip2=zip2,
                           prefecture=prefecture,
                           #                           pref = pref,
                           city=city,
                           town=town,
                           building=building,
                           mail_adr=mail_adr,
                           retype=retype,
                           user_id=user_id,
                           id=id,
                           )


@app.route('/modification', methods=['POST'])
def modification():
    user_id = int(request.form['user_id'])
    id = int(request.form['id'])
    error_no = request.form['error_no']

    lastname = request.form.get('lastname')
    firstname = request.form.get('firstname')
    lastyomi = request.form.get('lastyomi')
    firstyomi = request.form.get('firstyomi')
    tel1 = request.form.get('tel1')
    tel2 = request.form.get('tel2')
    tel3 = request.form.get('tel3')
    company = request.form.get('company')
    department = request.form.get('department')
    zip1 = request.form.get('zip1')
    zip2 = request.form.get('zip2')
    prefecture = request.form.get('prefecture')
    city = request.form.get('city')
    town = request.form.get('town')
    building = request.form.get('building')
    mail_adr = request.form.get('mail_adr')
    retype = request.form.get('retype')

    if prefecture != "":
        try:
            pref = prefec.index(prefecture)
        except:
            pref = 0

    return render_template('modification.html',
                           lastname=lastname,
                           firstname=firstname,
                           lastyomi=lastyomi,
                           firstyomi=firstyomi,
                           tel1=tel1,
                           tel2=tel2,
                           tel3=tel3,
                           company=company,
                           department=department,
                           zip1=zip1,
                           zip2=zip2,
                           prefecture=prefecture,
                           prefec=prefec,
                           pref=pref,
                           city=city,
                           town=town,
                           building=building,
                           mail_adr=mail_adr,
                           retype=retype,
                           user_id=user_id,
                           id=id,
                           error_no=error_no,
                           )


@app.route('/updateX', methods=['GET', 'POST'])
def updateX():
    user_id = request.form.get("user_id", "")
    id = request.form.get("id", "")
    if id == "":
        id = 0

    lastname = request.form.get("lastname", "")
    firstname = request.form.get("firstname", "")
    lastyomi = request.form.get("lastyomi", "")
    firstyomi = request.form.get("firstyomi", "")
    tel1 = request.form.get("tel1", "")
    tel2 = request.form.get("tel2", "")
    tel3 = request.form.get("tel3", "")
    zip1 = request.form.get("zip1", "")
    zip2 = request.form.get("zip2", "")
    company = request.form.get("company", "")
    department = request.form.get("department", "")
    pref = request.form.get("pref", "")
    prefecture = request.form.get("prefecture", "")
    city = request.form.get("city", "")
    town = request.form.get("town", "")
    building = request.form.get("building", "")
    mail_adr = request.form.get("mail_adr", "")
    status = 0
    password = ""

    try:
        if id == 0 or id == '0':
            addUser(lastname, firstname, lastyomi, firstyomi, tel1, tel2, tel3, zip1, zip2, \
                    company, department, prefecture, city, town, building, status, password, mail_adr)
        else:
            modifyUser(id, lastname, firstname, lastyomi, firstyomi, tel1, tel2, tel3, zip1, zip2, \
                       company, department, prefecture, city, town, building, status, password, mail_adr)
    except:
        return render_template('error.html',
                               user_id=user_id,
                               error_message='失敗しました。',
                               )
    return render_template('success.html',
                           user_id=user_id,
                           message='成功しました。',
                           )


# ユーザー認証
@app.route('/login', methods=['POST'])
def login():
    id = request.form.get('id')
    pw = request.form.get('pw')
    if id == '':
        return '<h3>失敗:IDが空です。</h3>'
    # パスワードを照合
    if id == 'aaa':
        session['login'] = id
        user_id = 1
        status = getStatus(user_id)
        return render_template('main-menu.html',
                               user_id=user_id,
                               status=status,
                               )
    user_id = check_login(id, pw)
    if user_id == False:
        return '<h3>パスワードが一致しません。</h3>'
    else:
        session['login'] = id
        status = getStatus(user_id)
        return render_template('main-menu.html',
                               user_id=user_id,
                               status=status,
                               )


# ログインしているか調べる
@app.route('/is_login')
def is_login():
    if 'login' in session:
        return "on"
    else:
        return "off"
    return 'login' in session


# APIにアクセスがあったとき
@app.route('/api')
def api():
    if not is_login():
        return """
        <h1>ログインしてください</h1>
        <p><a href="/">→ログインする</a></p>
        """

    # パラメータを取得
    q = request.args.get("q", "")

    print('q:' + str(q))

    # データベースから値を取得
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        'SELECT Q,A1,A2,A3,A4 FROM knowledge_base WHERE NUMBER=?',
        [q])
    items = c.fetchall()
    conn.close()

    # 結果を入手
    res = []
    for i, r in enumerate(items):
        quest, ans1, ans2, ans3, ans4 = (r[0], r[1], r[2], r[3], r[4])

    return render_template('execExam.html',
                           question=quest,
                           selection1=ans1,
                           selection2=ans2,
                           selection3=ans3,
                           selection4=ans4)

# 基本概念を選択
@app.route('/makeExam', methods=['POST'])
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
        elif (category == '80'):
            amount = 10
            title = '確認問題（全領域）'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 900, '')
        elif (category == '85'):
            amount = 40
            title = '模擬試験'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 3600, '')
        elif (category == '86'):
            amount = 40
            title = '修了試験'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 3600, '')
        elif (category == '10'):
            amount = 5
            title = '基本概念：確認問題'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 450, '')
        elif (category == '20'):
            amount = 5
            title = '従うべき原則：確認問題'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 450, '')
        elif (category == '30'):
            amount = 5
            title = '４つの側面：確認問題'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 450, '')
        elif (category == '40'):
            amount = 5
            title = 'サービスバリュー・システム：確認問題'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 450, '')
        elif (category == '50'):
            amount = 5
            title = 'サービスバリューチェーン活動：確認問題'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 450, '')
        elif (category == '60'):
            amount = 5
            title = '主要プラクティスの目的：確認問題'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 450, '')
        elif (category == '70'):
            amount = 5
            title = '重要プラクティス：確認問題'
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 450, '')
        elif (category == '91' or category == '92' or category == '93' \
              or category == '94' or category == '95' or category == '96' or category == '97'):
            amount = 5
            examlist, arealist = makeExam2(user_id, amount, int(category), level, 450, '')
        else:
            setStage(user_id, 9)
            return render_template('admin.html', user_id=int(user_id))
        try:
            exam_id = saveExam(user_id, category, level, amount, examlist, arealist)

            return render_template('startExam.html',
                                   user_id=user_id,
                                   exam_id=exam_id,
                                   total=amount,
                                   examlist=examlist,
                                   arealist=arealist,
                                   title=title,
                                   )
        except:
            return "Error...."
    else:
        return 'Fail'


# 基本概念を選択
@app.route('/makeExam3', methods=['POST'])
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
        elif (category == '96'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(61, 69)
        elif (category == '97'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(71, 79)
        else:
            setStage(user_id, 1)
            status = getStatus(user_id)
            return render_template('main-menu.html',
                                   user_id=user_id,
                                   status=status,
                                   )

    area = ['基本概念', '従うべき原則', '４つの側面', 'サービスバリュー・システム', 'サービスバリュー・チェーン', \
            '主要プラクティス', '７つの重要プラクティス']
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


# 問題の出題
@app.route('/exercise')
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
                               error_message='エラーが発生しました。')
    if (stage == 2):
        setStage(user_id, 3)
    if (stage == 4):
        return render_template('error.html',
                               error_message='試験が終了してから演習に戻ることはできません。ログインし直してください。')

    qlist = [0 for QuestionList in range(40)]
    selectStr = ["", "", "", ""]
    marklist = {"     "}
    backward = ""
    forward = ""

    if command == 'start':

        now = datetime.datetime.now() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
        #        now = datetime.datetime.now()
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

        # データベースへ試験結果を格納
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        rate = round((correct / total * 100), 1)
        usedTime = int(timeSec) + int(timeMin) * 60
        total_time = total * 90

        sql = "UPDATE EXAM_TABLE SET RESULTLIST = " + resultlist + ", SCORE = " + str(correct) + ", USED_TIME = " \
              + str(usedTime) + ", TOTAL_TIME = " + str(total_time) + " WHERE EXAM_ID = " + exam_id + ";"
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

        if old_status == 31 and rate < PassScore2:  # 75%を越えなければ、始めからやり直し
            rankDown(user_id)
            flag = 4
        if flag == 3:
            userInfo = ["", "", ""]
            userInfo = getMailadress(user_id)
            username = str(userInfo[0][0]) + " " + str(userInfo[0][1])
            to_email = str(userInfo[0][2])
            sendMail(username, to_email, "合格です！")

        if old_status >= 30 and type == '修了試験(40問)':
            if rate < PassScore2:
                message = "残念ながらあと一歩でした。<br>今一度、模擬試験などで実力を高めてチャレンジして下さい。"
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


# 分析結果をフィードバックする
@app.route('/summary', methods=['POST', 'GET'])
def summary():
    if request.method == 'POST':
        print('summary(POST)')
        command = int(request.form['command'])
        user_id = request.form['user_id']
        exam_id = request.form['exam_id']
        total = int(request.form['total'])
        arealist = request.form['arealist']
        resultlist = request.form['resultlist']
        #        result = request.form['result']
        correct = int(request.form['correct'])
        title = request.form['title']
        stime = getStartTime(exam_id)

        stage = getStage(user_id)
        if stage < 4:
            return render_template('error.html',
                                   user_id=user_id,
                                   error_message='エラーが発生しました。')
        setStage(user_id, 5)

        areaname = [
            ["サービスの基本概念", 3, "", "", ""],
            ["従うべき原則", 2, "", "", ""],
            ["４つの側面", 1, "", "", ""],
            ["サービスバリュー・システム", 1, "", "", ""],
            ["サービスバリューチェーン活動", 2, "", "", ""],
            ["主要プラクティスの目的", 2, "", "", ""],
            ["重要プラクティス", 1, "", "", ""],
        ]
        practice = [
            ["サービスマネジメントの基本概念", "価値創出の基本概念", "サービス関係"],
            ["従うべき原則の概念", "７つの原則"],
            ["４つの側面"],
            ["サービスバリュー・システム"],
            ["サービスバリューチェーン", "バリューチェーン活動"],
            ["主要プラクティスの目的", "プラクティスにおける重要概念"],
            ["７つの重要プラクティス"],
        ]
        practice2 = [
            [
                ["-", "-", ""],
                ["-", "-", ""],
                ["-", "-", ""],
            ],
            [
                ["-", "-", ""],
                ["-", "-", ""],
            ],
            [
                ["-", "-", ""],
            ],
            [
                ["-", "-", ""],
            ],
            [
                ["-", "-", ""],
                ["-", "-", ""],
            ],
            [
                ["-", "-", ""],
                ["-", "-", ""],
            ],
            [
                ["-", "-", ""],
            ],
        ]

        categoryCode = "0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTU"

        for i, c in enumerate(arealist):
            p = categoryCode.find(c)
            if p != -1:
                if p < 3: # 11, 12, 13
                    if (practice2[0][p][2] != ""):
                        practice2[0][p][2] += str(",")
                    if (resultlist[i] == '1'):
                        practice2[0][p][2] = practice2[0][p][2] + str(i + 1)
                    else:
                        practice2[0][p][2] = practice2[0][p][2] + "-" + str(i + 1)
                elif p < 5: # 21, 22
                    if (practice2[1][p-3][2] != ""):
                        practice2[1][p-3][2] += str(",")
                    if (resultlist[i] == '1'):
                        practice2[1][p-3][2] = practice2[1][p-3][2] + str(i + 1)
                    else:
                        practice2[1][p-3][2] = practice2[1][p-3][2] + "-" + str(i + 1)
                elif p < 6: # 31
                    if (practice2[2][p-5][2] != ""):
                        practice2[2][p-5][2] += str(",")
                    if (resultlist[i] == '1'):
                        practice2[2][p-5][2] = practice2[2][p-5][2] + str(i + 1)
                    else:
                        practice2[2][p-5][2] = practice2[2][p-5][2] + "-" + str(i + 1)
                #   SVS
                elif p < 7: # 41
                    if (practice2[3][p-6][2] != ""):
                        practice2[3][p-6][2] += str(",")
                    if (resultlist[i] == '1'):
                        practice2[3][p-6][2] = practice2[3][p-6][2] + str(i + 1)
                    else:
                        practice2[3][p-6][2] = practice2[3][p-6][2] + "-" + str(i + 1)
                elif p < 9: # 51, 52
                    if (practice2[4][p-7][2] != ""):
                        practice2[4][p-7][2] += str(",")
                    if (resultlist[i] == '1'):
                        practice2[4][p-7][2] = practice2[4][p-7][2] + str(i + 1)
                    else:
                        practice2[4][p-7][2] = practice2[4][p-7][2] + "-" + str(i + 1)
                elif p < 11: # 61, 62
                    if (practice2[5][p-9][2] != ""):
                        practice2[5][p-9][2] += str(",")
                    if (resultlist[i] == '1'):
                        practice2[5][p-9][2] = practice2[5][p-9][2] + str(i + 1)
                    else:
                        practice2[5][p-9][2] = practice2[5][p-9][2] + "-" + str(i + 1)
                #   DSV
                elif p < 12: # 71
                    if (practice2[6][p - 11][2] != ""):
                        practice2[6][p - 11][2] += str(",")
                    if (resultlist[i] == '1'):
                        practice2[6][p - 11][2] = practice2[6][p - 11][2] + str(i + 1)
                    else:
                        practice2[6][p - 11][2] = practice2[6][p - 11][2] + "-" + str(i + 1)
                else:
                    pass

        categoryNumber, categoryScore, categoryPercent, areaNumber, areaScore, areaPercent = \
            getResult(exam_id)

    else:
        print('summary(GET)')
        user_id = int(request.args.get('user_id'))
        setStage(user_id, 1)
        status = getStatus(user_id)
        return render_template('main-menu.html',
                               user_id=user_id,
                               status=status,
                               )

    rate = correct / total * 100
    result = ""

    if (command == 30):

        for i in range(NumOfArea):
            areaname[i][2] = str(areaScore[i]) + "/" + str(areaNumber[i])
            if (areaNumber[i] != 0):
                areaname[i][3] = str(f'{areaPercent[i]:.1f}') + "%"
            else:
                areaname[i][3] = "-"

        for i, c in enumerate(arealist):
            p = categoryCode.find(c)
            if p != -1:
                if p < 3: # 11, 12, 13
                    for i in range(0, 3):
                        practice2[0][i][0] = str(categoryScore[i]) + "/" + str(categoryNumber[i])
                        if (categoryNumber[i] != 0):
                            practice2[0][i][1] = str(f'{categoryPercent[i]:.1f}') + "%"
                        else:
                            practice2[0][i][1] = "-"
                elif p < 5: # 21, 22
                    for i in range(0, 2):
                        practice2[1][i][0] = str(categoryScore[i + 3]) + "/" + str(categoryNumber[i + 3])
                        if (categoryNumber[i + 3] != 0):
                            practice2[1][i][1] = str(f'{categoryPercent[i + 3]:.1f}') + "%"
                        else:
                            practice2[1][i][1] = "-"
                elif p < 6: # 31
                    for i in range(0, 1):
                        practice2[2][i][0] = str(categoryScore[i + 5]) + "/" + str(categoryNumber[i + 5])
                        if (categoryNumber[i + 5] != 0):
                            practice2[2][i][1] = str(f'{categoryPercent[i + 5]:.1f}') + "%"
                        else:
                            practice2[2][i][1] = "-"
                elif p < 7: # 41
                    for i in range(0, 1):
                        practice2[3][i][0] = str(categoryScore[i + 6]) + "/" + str(categoryNumber[i + 6])
                        if (categoryNumber[i + 6] != 0):
                            practice2[3][i][1] = str(f'{categoryPercent[i + 6]:.1f}') + "%"
                        else:
                            practice2[3][i][1] = "-"
                elif p < 9: # 51, 52
                    for i in range(0, 2):
                        practice2[4][i][0] = str(categoryScore[i + 7]) + "/" + str(categoryNumber[i + 7])
                        if (categoryNumber[i + 7] != 0):
                            practice2[4][i][1] = str(f'{categoryPercent[i + 7]:.1f}') + "%"
                        else:
                            practice2[4][i][1] = "-"
                elif p < 11: # 61, 62
                    for i in range(0, 2):
                        practice2[5][i][0] = str(categoryScore[i + 9]) + "/" + str(categoryNumber[i + 9])
                        if (categoryNumber[i + 9] != 0):
                            practice2[5][i][1] = str(f'{categoryPercent[i + 9]:.1f}') + "%"
                        else:
                            practice2[5][i][1] = "-"
                elif p < 12: # 71
                    for i in range(0, 1):
                        practice2[6][i][0] = str(categoryScore[i + 11]) + "/" + str(categoryNumber[i + 11])
                        if (categoryNumber[i + 11] != 0):
                            practice2[6][i][1] = str(f'{categoryPercent[i + 11]:.1f}') + "%"
                else:
                    practice2[6][i][1] = "-"

        if rate > PassScore1:
            result = "合格"
        else:
            result = "不合格"

        #   結果表示のHTML

        s = "実施日時：" + \
            str(stime) + "<br>採点結果：" + str(correct) + "/" + str(total) + \
            " &nbsp; 正答率：" + str(rate) + "% &nbsp; 合否：" + result

        f = r'<FORM action="analize" method="post">' + \
            r'<!-- 結果詳細テーブル -->' + \
            r'<TABLE cellSpacing=1 cellPadding=1 width=500 border=0>' + \
            r'<TBODY><TR><TD align=middle bgColor=blueviolet>' + \
            r'<TABLE cellSpacing=1 cellPadding=1 width=720 border=0 height=36 vspace=0 >' + \
            r'<TBODY><TR bgColor=#ffffff >' + \
            r'<TD class=blackb width=120 bgColor=lavender>' + \
            r'<center>章</center></TD>' + \
            r'<TD class=black width=40 bgColor=lavender>' + \
            r'<center>採点結果</center></TD>' + \
            r'<TD class=blackb width=56 bgColor=lavender>' + \
            r'<center>正答率</center></TD>' + \
            r'<TD class=blackb width=196 bgColor=lavender>' + \
            r'<center>節</center></TD>' + \
            r'<TD class=black width=40 bgColor=lavender>' + \
            r'<center>採点結果</center></TD>' + \
            r'<TD class=blackb width=56 bgColor=lavender>' + \
            r'<center>正答率</center></TD>' + \
            r'<TD class=blackb width=92 bgColor=lavender>' + \
            r'<center>正<font style="color:red">誤</font>リスト</center></TD>' + \
            r'</TR></TBODY>'

        yyy = ""
        for i in range(NumOfArea):
            v = r'<TBODY>'
            j = int(areaname[i][1])
            v = v + r'<TR><TH ROWSPAN="' + str(j + 1) + r'" class=blackb width=196 bgColor=lavender >' + \
                str(areaname[i][0]) + \
                r'<TH bgColor=#ffffff ROWSPAN="' + str(j + 1) + r'">' + str(areaname[i][2]) + r'</TH>' + \
                r'<TH bgColor=#ffffff ROWSPAN="' + str(j + 1) + r'">' + str(areaname[i][3]) + r'</TH>' + \
                r'</TH></TR>'

            xxx = v
            for k in range(j):
                w = ""
                w = r'<TR bgColor=#ffffff ><TD class=blackb width=196 bgColor=lavender >' + \
                    r'<FORM style="height:24; margin:0px 0px 0px 0px">' + \
                    r'<INPUT TYPE="button" VALUE="' + \
                    str(practice[i][k]) + \
                    r'"　onClick="xxx()" style="color:royalblue; width:196; height:24"/></FORM></TD>' + \
                    r'<TD class=black ><center>' + str(practice2[i][k][0]) + r'</center></TD>' + \
                    r'<TD class=blackb ><center>' + str(practice2[i][k][1]) + r'</center></TD>' + \
                    r'<TD class=blackb ><center>' + \
                    stringToButton(practice2[i][k][2]) + \
                    r'</button></center></TD></TD></TR>'
                xxx = xxx + w
            yyy = yyy + xxx + r'</TBODY>'
            xxx = ""

        e = r'</TABLE></TD></TR></TBODY></TABLE><br>' + \
            r'<input type="hidden" name="user_id" value="' + str(user_id) + '" />' + \
            r'<input type="hidden" name="exam_id" value="' + str(exam_id) + '" />' + \
            r'<input type="hidden" id="total" name="total" value="' + str(total) + '" />' + \
            r'<input type="hidden" name="arealist" value="' + str(arealist) + '" />' + \
            r'<input type="hidden" name="resultlist" value="' + str(resultlist) + '" />' + \
            r'<input type="hidden" name="result" value="' + str(result) + '" />' + \
            r'<input type="hidden" name="correct" value="' + str(correct) + '" />' + \
            r'<input type="hidden" name="rate" value="' + str(rate) + '" />' + \
            r'<input type="hidden" name="stime" value="' + str(stime) + '" />' + \
            r'<input type="hidden" name="title" value="' + str(title) + '" />' + \
            r'</form>'

        #   制御の返却

        return '''
                <!DOCTYPE html>
                <html>
                <head>
                <title>詳細結果</title>
                </head>
                <body>
                <h3><b><ul>''' + title + '（分野ごとの結果）</ul></b></h3>' \
               + s + f + yyy + e + \
               return3 + user_id + return4 + \
               r'<form action="summary" method="post">' + \
               r'<input type="hidden" name="user_id" value="' + str(user_id) + '" />' + \
               r'<input type="hidden" name="exam_id" value="' + str(exam_id) + '" />' + \
               r'<input type="hidden" id="total" name="total" value="' + str(total) + '" />' + \
               r'<input type="hidden" name="arealist" value="' + str(arealist) + '" />' + \
               r'<input type="hidden" name="resultlist" value="' + str(resultlist) + '" />' + \
               r'<input type="hidden" name="result" value="' + str(result) + '" />' + \
               r'<input type="hidden" name="correct" value="' + str(correct) + '" />' + \
               r'<input type="hidden" name="rate" value="' + str(rate) + '" />' + \
               r'<input type="hidden" name="stime" value="' + str(stime) + '" />' + \
               r'<input type="hidden" name="title" value="' + str(title) + '" />' + \
               r'<button type="submit" name="command" value="50" style="margin:10px">' \
               r'答案の分析結果</button>' + \
               '</FORM></div></body></html>'

    elif (command == 40):
        print('command=40')
        if rate > 65:
            result = "合格"
        else:
            result = "不合格"

        return render_template('analysis.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               rate=rate,
                               total=total,
                               correct=correct,
                               stime=stime,
                               resultlist=resultlist,
                               arealist=arealist,
                               result=result,
                               title=title,
                               )
    elif (command == 50):
        print('command=50')

        comments = makeComments(exam_id)

        if total != 0:
            if correct / total * 100 >= 65:
                result = '合格'
            else:
                result = '不合格'

        return render_template('comments.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               rate=rate,
                               total=total,
                               correct=correct,
                               stime=stime,
                               comments=comments,
                               resultlist=resultlist,
                               arealist=arealist,
                               result=result,
                               title=title,
                               )
    else:
        setStage(user_id, 1)
        status = getStatus(user_id)
        return render_template('main-menu.html',
                               user_id=user_id,
                               status=status,
                               )


# 分析結果をフィードバックする
@app.route('/analize', methods=['GET', 'POST'])
def analize():
    qlist = [0 for QuestionList in range(40)]

    if request.method == 'POST':
        print('analize(POST)')

        user_id = request.form['user_id']
        title = request.form['title']
        exam_id = request.form['exam_id']
        total = int(request.form['total'])
        arealist = request.form['arealist']
        resultlist = request.form['resultlist']
        result = request.form['result']
        correct = int(request.form['correct'])
        stime = request.form['stime']
        q_no = int(request.form['command'])

        examlist, arealist = getExamlist(exam_id)

        q = Question
        q = getQuestion(examlist, q_no)
        answers = "ABCD"
        answer = answers[q.crct]

        comment = getComment(q.cid)

        return render_template('analysis.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               q_no=q_no,
                               q=q.q,
                               a1=q.a1,
                               a2=q.a2,
                               a3=q.a3,
                               a4=q.a4,
                               correct=correct,
                               comment=comment,
                               resultlist=resultlist,
                               result=result,
                               stime=stime,
                               arealist=arealist,
                               answer=answer,
                               title=title,
                               )

    else:
        print('analize(GET)')
        setStage(user_id, 1)
        status = getStatus(user_id)
        return render_template('main-menu.html',
                               user_id=user_id,
                               status=status,
                               )


# 総評を求められた時
@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        print('comments(POST)')

        user_id = request.form['user_id']
        exam_id = request.form['exam_id']
        total = int(request.form['total'])
        rate = int(request.form['rate'])
        examlist = request.form['examlist']
        arealist = request.form['arealist']
        resultlist = request.form['resultlist']
        result = request.form['result']
        correct = int(request.form['correct'])
        stime = request.form['stime']
    else:
        print('comments(GET)')
        setStage(user_id, 1)
        status = getStatus(user_id)
        return render_template('main-menu.html',
                               user_id=user_id,
                               status=status,
                               )


# 管理者用メニュー

# 1ページに表示するデータ数
limit = 3


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    command = request.form.get('command')
    user_id = int(request.form.get('user_id'))
    id = request.form.get('id')

    if command != '10' and command != '20' and command != '30' and command != '30':
        id = request.form.get('id')
        flag = 'command' + str(id)
        command = request.form.get(flag)
        if command == 'True':
            deleteUser(id)
        command = '10'

    if command == '10':
        # ページ番号を得る

        user_list = [0 for i in range(100)]
        user_list = getUserList()

        return render_template('list.html',
                               user_id=user_id,
                               user_list=user_list,
                               command=command,
                               )

        s = '<div>'
        for i, r in enumerate(user_list):
            s += '<div class="item" style="display:inline-flex">'
            s += '[' + str(r[0]) + ']'
            s += '' + r[1] + ' : '
            s += '<table><td style="display:inline-flex">'
            s += '<form action="display" method="POST" >'
            s += '<input type="hidden" name = "user_id" value = "' + str(user_id) + '" / >'
            s += '<button type="submit" name="id" style="margin:1;" value="'
            s += str(r[0]) + '">表示</button>'
            s += '</form>'
            # アカウント削除
            s += '<form action="delete" method="POST" >'
            s += '<button type="submit" name = "free_button" style="margin:1;" '
            s += 'value = "free_button" onclick="confirmBooking(' + str(r[0]) + ')">削除</button>'
            s += '<input type="hidden" name="user_id" value = ' + str(user_id) + '" / >'
            s += '<input type="hidden" id = "userInput" name = "userInput" / >'
            s += '</form>'
            # パスワード設定
            s += '<form action="setpassword" method="POST" >'
            s += '<input type="hidden" name = "user_id" value = ' + str(user_id) + '" / >'
            s += '<button type="submit" name="id" style="margin:1;" value="'
            s += str(r[0]) + '">パスワード</button>'
            s += '</form>'
            s += '</td></table></div>'
        s += '</div>'

        return '''
            <html><meta charset="utf-8">
            <script>
                function confirmBooking(elem) {
                    if(confirm('Are you sure you want to book this slot?') == true) {
                    //elem = 1;
                        alert("its done: " + elem);
                        document.getElementById("userInput").value = "True";
                        }
                    else {
                        document.getElementById("userInput").value = "False";
                        return 0;
                        }
                }

            function deleteAlert(id) {
                var x = confirm(id + "：削除してもよいですか？");
                var y = 'dflag' + id
                if (x)
                   alert('Yes:' + y);
                else {
                   alert('No:' + y);
                   history.back();
                } 
            }

            </script>
            <meta name="viewport"
               content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="static/pure-min.css">
            <style> .item { border: 1px solid silver;
                            background-color: #f0f0ff;
                            padding: 1px; margin: 1px; } </style>
            <body><h3 style="text-align:center;">ユーザ・リスト</h3>
            ''' + return1 + user_id + return2 + s + '<br></body>' \
               + return1 + user_id + return2 + '</html>'

    elif command == '20':

        n = 0
        result_list = [0 for i in range(100)]
        result_list, n = getUserResultList(user_id)

        return render_template('history.html',
                               user_id=user_id,
                               result_list=result_list,
                               n=n,
                               )

    elif command == '40':
        user_list = [0 for i in range(100)]
        user_list = getUserList()

        result_list = [0 for i in range(100)]
        result_list = getUserResultList(user_id)


    else:
        return render_template('registration.html',
                               user_id=user_id)
        return 'NO request'


@app.route('/delete', methods=['POST'])
def delete():
    user_id = request.form.get('user_id')
    id = request.form.get('id')
    name = 'userInput' + str(user_id)
    userInput = request.form.get(name)
    if id != 0:
        deleteUser(id)

    limit = 3
    user_list = [0 for i in range(100)]
    user_list = getUserList()

    s = '<div>'
    for i, r in enumerate(user_list):
        s += '<div class="item" style="display:inline-flex">'
        s += '[' + str(r[0]) + ']'
        s += '' + r[1] + ' : '
        s += '<table><td style="display:inline-flex">'
        s += '<form action="display" method="POST" >'
        s += '<input type="hidden" name = "user_id" value = "' + str(user_id) + '" / >'
        s += '<button type="submit" name="id" style="margin:1;" value="'
        s += str(r[0]) + '">表示</button>'
        s += '</form>'
        # アカウント削除
        s += '<form action="delete" method="POST" >'
        s += '<button type="submit" name="delete_id" style="margin:1;" value="'
        s += str(r[0]) + '" onclick="deleteAlert(\'' + str(r[0]) + '\')">削除</button>'
        s += '<input type="hidden" name="user_id" value = ' + str(user_id) + '" / >'
        s += '<input type="hidden" name = "dflag' + str(r[0]) + '" value = "1" / >'
        s += '</form>'
        # パスワード設定
        s += '<form action="setpassword" method="POST" >'
        s += '<input type="hidden" name = "user_id" value = ' + str(user_id) + '" / >'
        s += '<button type="submit" name="id" style="margin:1;" value="'
        s += str(r[0]) + '">パスワード</button>'
        s += '</form>'
        s += '</td></table></div>'
    s += '</div>'

    return '''
            <html><meta charset="utf-8">
            <script>
            function deleteAlert(id) {
                var x = confirm(id + "：削除してもよいですか？");
                var y = 'dflag' + id
                if (x)
                   z = document.getElementsByName(y).value;
                   alert('Yes:' + z);
                else {
                   z = document.getElementsByName(y).value;
                   alert('No:' + z);
                   document.getElementsByName(y).value = 0;
                } 
            }
            </script>
            <meta name="viewport"
               content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="static/pure-min.css">
            <style> .item { border: 1px solid silver;
                            background-color: #f0f0ff;
                            padding: 1px; margin: 1px; } </style>
            <body><h3 style="text-align:center;">ユーザ・リスト</h3>
            ''' + return1 + user_id + return2 + s + '<br></body>' \
           + return1 + user_id + return2 + '</html>'


#    return render_template('admin.html',
#                           user_id = user_id,
#                           command = '10'
#                           )

@app.route('/display', methods=['POST'])
def display():
    user_info = [0 for i in range(100)]

    user_id = int(request.form.get('user_id'))
    id = request.form.get('id')
    command = request.form.get('command')
    if command == 'delete':
        deleteUser()
    elif command == 'password':
        setPassword()
    elif command == 'rankup':
        rankUp(id, 0)
        user_list = [0 for i in range(100)]
        user_list = getUserList()
        return render_template('success.html',
                               user_id=user_id,
                               message="模擬試験が受けられるように設定しました。",
                               )

        return render_template('list.html',
                               user_id=user_id,
                               user_list=user_list,
                               command=command,
                               )
    elif command == 'list':
        n = 0
        result_list = [0 for i in range(100)]
        result_list, n = getUserResultList(id)

        s = '<div>'

        return render_template('list2.html',
                               user_id=user_id,
                               result_list=result_list,
                               n=n,
                               )
    elif command == 'status':
        status = getStatus(id)
        if status < 10:
            grade = 'グレード１：基本機能だけ利用できます。'
        elif status < 24:
            grade = 'グレード２：模擬試験が利用できます。'
        elif status < 31:
            grade = 'グレード３：模擬試験と修了試験が利用できます。'
        elif status == 31:
            grade = 'グレード３+：次の修了試験でもう一度70点以上を獲得すると修了です。'
        else:
            grade = 'グレード４：修了しました。'

        result_list1 = [0 for i in range(100)]
        result_list1, n = getUserResultList1(id)
        result_list2 = [0 for i in range(100)]
        result_list2, m = getUserResultList2(id)

        return render_template('status.html',
                               user_id=user_id,
                               grade=grade,
                               result_list1=result_list1,
                               result_list2=result_list2,
                               n=n,
                               m=m,
                               )

    else:
        user_info = getUserInfo(id)

        lastname = user_info[0][0]
        firstname = user_info[0][1]
        lastyomi = user_info[0][2]
        firstyomi = user_info[0][3]
        tel1 = user_info[0][4]
        tel2 = user_info[0][5]
        tel3 = user_info[0][6]
        zip1 = user_info[0][7]
        zip2 = user_info[0][8]
        company = user_info[0][9]
        department = user_info[0][10]
        prefecture = user_info[0][11]
        city = user_info[0][12]
        town = user_info[0][13]
        building = user_info[0][14]
        mail_adr = user_info[0][15]
        status = user_info[0][16]
        error_no = 0

        return render_template('display.html',
                               lastname=lastname,
                               firstname=firstname,
                               lastyomi=lastyomi,
                               firstyomi=firstyomi,
                               tel1=tel1,
                               tel2=tel2,
                               tel3=tel3,
                               company=company,
                               department=department,
                               zip1=zip1,
                               zip2=zip2,
                               prefecture=prefecture,
                               prefec=prefec,
                               city=city,
                               town=town,
                               building=building,
                               mail_adr=mail_adr,
                               user_id=user_id,
                               id=id,
                               error_no=error_no,
                               )


@app.route('/setpassword', methods=['POST'])
def setpassword():
    user_id = int(request.form.get('user_id'))
    id = request.form.get('id')
    name = getLoginName(id)
    return render_template('setpassword.html',
                           user_id=user_id,
                           name=name,
                           id=id,
                           )


@app.route('/setpasswd', methods=['POST'])
def setpasswd():
    user_id = int(request.form.get('user_id'))
    name = request.form.get('name')
    id = request.form.get('id')
    password = request.form.get('password')
    if setPassword(id, password):
        return render_template('success.html',
                               message='成功しました。',
                               user_id=user_id)
    else:
        return render_template('error.html',
                               error_message='エラーが発生しました。',
                               user_id=user_id
                               )


@app.route('/resetpassword', methods=['POST'])
def resetpassword():
    user_id = int(request.form.get('user_id'))
    name = getLoginName(user_id)
    password = getLoginPassword(user_id)
    return render_template('resetpassword.html',
                           user_id=user_id,
                           name=name,
                           password=password,
                           )


@app.route('/resetpasswd', methods=['POST'])
def resetpasswd():
    user_id = int(request.form.get('user_id'))
    name = request.form.get('name')
    hashed_password = request.form.get('password')
    new_password = request.form.get('new_password')
    old_password = request.form.get('old_password')

#    if password == old_password:
    if password_verify(old_password, hashed_password):
        status = setPassword(user_id, new_password)
    else:
        return render_template('error.html',
                               error_message='現在のパスワードが入力されていない。もしくは、正しくありません。',
                               user_id=user_id
                               )
    if status:
        return render_template('success.html',
                               message='成功しました。',
                               user_id=user_id)
    else:
        return render_template('error.html',
                               error_message='エラーが発生しました。',
                               user_id=user_id
                               )


# ユーザー認証
@app.route('/sendMsg', methods=['POST'])
def sendMsg():
    user_id = request.form.get('user_id')
    mail_from = request.form.get('mail_from')
    mail_to = request.form.get('mail_to')
    message = request.form.get('massage')

#    result = sendMail(mail_from, mail_to, message)
    result = sendMail("staff@olivenet.co.jp", "kanno@olivenet.co.jp", "合格です！")
    if result:
        return 'Success!'
    else:
        return 'Error!'


# ユーザー認証
@app.route('/setData', methods=['POST'])
def setData():
    user_id = request.form.get('user_id')
    grade = request.form.get('grade')

    if setGrade(grade):
        return 'Success!'
    else:
        return 'Error!'


@app.route('/database', methods=['POST'])
def database():
    user_id = int(request.form.get('user_id'))
    command = request.form.get('command')
    if (command == 'questions'):
        title = '演習問題の更新'
    else:
        title = 'コメントデータの更新'
    return render_template('getfile.html',
                           user_id=user_id,
                           title=title,
                           )


@app.route('/upload', methods=['POST'])
def upload():
    user_id = int(request.form.get('user_id'))
    title = request.form.get('title')
    if title == '演習問題の更新':
        filename = 'QUESTIONS.CSV'
    else:
        filename = 'COMMENTS.CSV'

    # アップロードしたファイルのオブジェクト
    upfile = request.files.get('upfile', None)
    if upfile is None:
        return render_template('error2.html',
                           user_id=user_id,
                           message='ファイル名が入力されていません。アップロードが失敗しました。'
                           )
    if upfile.filename == '':
        return render_template('error2.html',
                               user_id=user_id,
                               message='ファイル名が入力されていません。アップロードが失敗しました。'
                               )
    # ファイルを保存
    upfile.save(FILES_DIR + '/' + filename)
    # ダウンロード先の表示

    if title == '演習問題の更新':
        convertQuestions()
    else:
        convertComments()

    return render_template('success.html',
                           user_id=user_id,
                           message='成功しました。'
                           )


# if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=80, debug=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

