from constant import db_path, FILES_DIR
import sqlite3, csv
from flask import Flask, render_template, request, Blueprint

database_module = Blueprint("database", __name__, static_folder='./static')

@database_module.route('/database', methods=['POST'])
def database():
    user_id = int(request.form.get('user_id'))
    command = request.form.get('command')
    if (command == 'download'):
        title = '演習問題のダウンロード'
        return render_template('download.html',
                               user_id=user_id,
                               )
    elif (command == 'questions'):
        title = '演習問題の更新'
    elif (command == 'comments'):
        title = 'コメントデータの更新'
    else:
        return render_template('maintenance.html',
                               user_id=user_id,
                               )
    return render_template('getfile.html',
                           user_id=user_id,
                           title=title,
                           )


@database_module.route('/upload', methods=['POST'])
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

@database_module.route('/download', methods=['POST'])
def download():
    user_id = int(request.form.get('user_id'))

    result = retrieveData()
    if (result == 1):
        return render_template('download2.html',
                           user_id=user_id,
                           message='成功しました。'
                           )
    else:
        return render_template('error2.html',
                           user_id=user_id,
                           message='失敗しました。'
                           )

def convertQuestions():

    # DBに接続してテーブルを作成
    conn = sqlite3.connect(db_path)
    conn.execute("DROP TABLE IF EXISTS knowledge_base")
    conn.execute('''
      CREATE TABLE IF NOT EXISTS knowledge_base (
        number INTEGER PRIMARY KEY,
        category INTEGER,
        level INTEGER,
        q TEXT,
        a1 TEXT,
        a2 TEXT,
        a3 TEXT,
        a4 TEXT,
        cid1 INTEGER,
        cid2 INTEGER,
        cid3 INTEGER,
        cid4 INTEGER,
        flag INTEGER
      )
    ''')

    read_csv(conn, FILES_DIR + '/QUESTIONS.CSV')
    return

# CSVを読んでDBに入れる関数
def read_csv(conn, fname):
    c = conn.cursor()
    f = open(fname, encoding='cp932')
#    f = open(fname, encoding='shift-jis')
#    f = open(fname, encoding='utf_8')
    reader = csv.reader(f)
    for row in reader:
        number = int(row[0])
        category = row[2]
        level = row[1]
        q = row[3]
        a1 = row[4]
        a2 = row[5]
        a3 = row[6]
        a4 = row[7]
        cid1 = row[8]
        cid2 = row[9]
        cid3 = row[10]
        cid4 = row[11]
        flag = row[12]
        print(q)
        c.execute(
            'INSERT INTO knowledge_base (number, category, level, q, a1, a2, a3, a4, cid1, cid2, cid3, cid4, flag) ' +
            'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
            [number, category, level, q, a1, a2, a3, a4, cid1, cid2, cid3, cid4, flag])
    f.close()
    conn.commit()
    conn.close()
    return

def convertComments():
    # DBに接続してテーブルを作成
    conn = sqlite3.connect(db_path)
    conn.execute("DROP TABLE IF EXISTS comments_table")
    conn.execute('''
      CREATE TABLE IF NOT EXISTS comments_table (
        comment_id INTEGER PRIMARY KEY,
        comment TEXT
      )
    ''')

    read_comments_csv(conn, FILES_DIR + '/COMMENTS.CSV')
    return

# コメント・データをDBに入れる関数
def read_comments_csv(conn, fname):
        c = conn.cursor()
        f = open(fname, encoding='cp932')
        #    f = open(fname, encoding='shift-jis')
        #    f = open(fname, encoding='utf_8')
        reader = csv.reader(f)
        for row in reader:
            comment_id = int(row[0])
            comment = row[1]
            print(comment_id)
            conn.execute(
                'INSERT INTO comments_table ( comment_id, comment) ' +
                'VALUES (?, ?)',
                [comment_id, comment])
        f.close()
        conn.commit()
        conn.close()
        return

def retrieveData():
    # DBに接続してテーブルを作成
    qfile = FILES_DIR + '/questions.csv'
    cfile = FILES_DIR + '/comments.csv'

    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
    #    cursor.execute("SELECT * FROM knowledge_base") # levelが「area」になっている（2022,12,25）
        cursor.execute("SELECT number,level,category,q,a1,a2,a3,a4,cid1,cid2,cid3,cid4,flag FROM knowledge_base")
        with open( qfile , "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow([i[1] for i in cursor.description])
            csv_writer.writerows(cursor)

        cursor.execute("SELECT * FROM comments_table")
        with open( cfile , "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow([i[1] for i in cursor.description])
            csv_writer.writerows(cursor)

    except:
        conn.close()
        return -1
    else:
        conn.close()
        return 1
